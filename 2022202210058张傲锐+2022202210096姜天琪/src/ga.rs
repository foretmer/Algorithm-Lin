use rand::prelude::*;
use rayon::prelude::*;
use serde::*;

use crate::{utils::Position, solver::Transcoder};

#[derive(Clone)]
struct Individual {
    genes: Vec<f32>,
    solution: (f32, Vec<Position>),
    fitness: f64,
}

#[derive(Copy, Clone, Debug, Serialize, Deserialize)]
pub struct Params {
    pub population_factor: usize,
    pub elites_percentage: f64,
    pub mutants_percentage: f64,
    pub inherit_probability: f64,
    pub max_generations: i32,
    pub max_generations_no_improvement: i32,
    pub population_size: usize,
    pub num_elites: usize,
    pub num_mutants: usize,
}

impl Default for Params {
    fn default() -> Self {
        Params {
            population_factor: 30,
            elites_percentage: 0.10,
            mutants_percentage: 0.15,
            inherit_probability: 0.70,
            max_generations: 200,
            max_generations_no_improvement: 5,
            population_size: 0,
            num_elites: 0,
            num_mutants: 0,
        }
    }
}

impl Params {
    pub fn get_params(&mut self, num_items: usize) {
        let population_size = self.population_factor * num_items;
        let num_elites = (self.elites_percentage * population_size as f64) as usize;
        let num_mutants = (self.mutants_percentage * population_size as f64) as usize;
        self.population_size = population_size;
        self.num_elites = num_elites;
        self.num_mutants = num_mutants;
    }
}

#[derive(Copy, Clone, Debug)]
pub struct RandGenerator {
    length: usize,
}

impl RandGenerator {
    pub fn new(length: usize) -> RandGenerator {
        RandGenerator { length }
    }

    pub fn breed(&self) -> Vec<f32> {
        let mut rng = thread_rng();
        (0..self.length).map(|_| rng.gen()).collect()
    }
}

pub struct EvolutionaryAlgorithm<F>
where
    F: Fn() -> Transcoder,
{
    generator: RandGenerator,
    transcoder_factory: F,
    params: Params,
    pop: Vec<Individual>,
}

impl<F> EvolutionaryAlgorithm<F>
where
    F: Fn() -> Transcoder + Sync + Send,
{
    pub fn new(
        params: Params,
        generator: RandGenerator,
        transcoder_factory: F,
    ) -> EvolutionaryAlgorithm<F> {
        EvolutionaryAlgorithm {
            generator,
            transcoder_factory,
            params,
            pop: Vec::with_capacity(params.population_size),
        }
    }

    pub fn solve(&mut self) -> (f32, Vec<Position>) {
        let mut generation = 0;
        let mut generations_no_improvement = 0;

        self.init();

        while generation < self.params.max_generations
            && generations_no_improvement < self.params.max_generations_no_improvement
        {
            let prev_fitness = self.pop[0].fitness;
            self.evolve();
            let curr_fitness = self.pop[0].fitness;

            if curr_fitness < prev_fitness {
                generations_no_improvement = 0;
            } else {
                generations_no_improvement += 1;
            }

            generation += 1;
        }

        self.pop[0].solution.clone()
    }

    fn evolve(&mut self) {
        let num_elites = self.params.num_elites;
        let num_mutants = self.params.num_mutants;
        let num_offsprings = self.params.population_size - num_elites - num_mutants;

        let transcoder_factory = &self.transcoder_factory;
        let generator = &self.generator;

        let mut new_pop: Vec<_> = (0..(num_mutants + num_offsprings))
            .into_par_iter()
            .map(|i| {
                let mut transcoder = transcoder_factory();
                if i < num_mutants {
                    Self::transcode_gene(&mut transcoder, generator.breed())
                } else {
                    let mut rng = thread_rng();
                    let non_elite_size = self.params.population_size - self.params.num_elites;
                    let elite = &self.pop[rng.gen_range(0..self.params.num_elites)].genes;
                    let non_elite =
                        &self.pop[self.params.num_elites + rng.gen_range(0..non_elite_size)].genes;
                    let mut offspring = Vec::with_capacity(elite.len());
                    offspring.extend((0..elite.len()).map(|i| {
                        let p: f64 = rng.gen();
                        if p <= self.params.inherit_probability {
                            elite[i]
                        } else {
                            non_elite[i]
                        }
                    }));
                    Self::transcode_gene(&mut transcoder, offspring)
                }
            })
            .collect();

        for elite in &self.pop[0..num_elites] {
            new_pop.push(elite.clone());
        }
        new_pop.sort_unstable_by(|a, b| a.fitness.partial_cmp(&b.fitness).unwrap());
        self.pop = new_pop;
    }

    fn init(&mut self) {
        let decoder_factory = &self.transcoder_factory;
        let generator = &self.generator;
        self.pop = (0..self.params.population_size)
            .into_par_iter()
            .map(|_| {
                let mut decoder = decoder_factory();
                Self::transcode_gene(&mut decoder, generator.breed())
            })
            .collect();
        self.pop
            .sort_unstable_by(|a, b| a.fitness.partial_cmp(&b.fitness).unwrap());
    }

    #[inline]
    fn transcode_gene(decoder: &mut Transcoder, genes: Vec<f32>) -> Individual {
        let solution = decoder.transcoder(&genes);
        let fitness = decoder.fitness(&solution);
        decoder.reset();

        Individual {
            genes,
            solution,
            fitness,
        }
    }
}
