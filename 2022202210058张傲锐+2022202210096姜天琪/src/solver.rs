use std::cell::RefCell;
use std::f32;

use crate::utils::*;
use crate::object::*;

pub struct Transcoder {
    bin_volume: f32,
    solver: Solver,
}

impl Transcoder {
    pub fn new<'a, T: 'a>(boxes: &'a [T], bin_spec: Cuboid) -> Self
    where
        &'a T: Into<Cuboid>,
    {
        let boxes = boxes.iter().map(|b| b.into().into()).collect();
        let bin_volume = bin_spec.volume();
        let solver = Solver::new(boxes, bin_spec);
        Self { solver, bin_volume }
    }

    pub fn transcoder(&mut self, individual: &Vec<f32>) -> (f32, Vec<Position>) {
        self.solver.arrange(individual)
    }

    pub fn fitness(&self, solution: &(f32, Vec<Position>)) -> f64 {
        solution.0 as f64 / self.bin_volume as f64
    }

    pub fn reset(&mut self) {
        self.solver.reset();
    }
}

struct Solver {
    boxes: Vec<Box>,
    bins: BinList,
    orient: RefCell<Vec<Cuboid>>,
}

#[allow(unused_assignments)]
impl Solver {
    fn new(boxes: Vec<Box>, bin_cuboid: Cuboid) -> Self {
        Solver {
            boxes,
            bins: BinList::new(bin_cuboid),
            orient: RefCell::new(Vec::new()),
        }
    }
    fn reset(&mut self) {
        self.bins.reset();
        self.orient.borrow_mut().clear();
    }

    fn arrange(&mut self, gene: &Vec<f32>) -> (f32, Vec<Position>) {
        let mut positions = Vec::with_capacity(self.boxes.len());
        let (mut min_dim, mut min_volume) = (f32::MAX, f32::MAX);
        let mut bps = Vec::new();
        bps = (0..gene.len() / 2).collect::<Vec<usize>>();
        bps.sort_by(|&a, &b| {
            self.boxes[b]
                .volume
                .partial_cmp(&self.boxes[a].volume)
                .unwrap()
        });
        for (box_position_strategy_index, &inner_box_index) in bps.iter().enumerate() {
            let to_pack = &self.boxes[inner_box_index];
            let (mut fit_bin, mut fit_space) = (0, None);
            let fit_bin_index = self.bins.opened().iter().enumerate().find(|(_, bin)| {
                let position = bin.try_encase(&to_pack.cuboid);
                if let Some(space) = position {
                    fit_space = Some(space);
                    true
                } else {
                    false
                }
            });

            if let Some((bin_index, _)) = fit_bin_index {
                fit_bin = bin_index;
            } else {
                let new_bin_index = self.bins.create_bin();
                fit_bin = new_bin_index;
                let new_bin = &self.bins.bins[new_bin_index];
                fit_space = Some(&new_bin.empty_list[0]);
            }

            let fit_space = fit_space.unwrap();
            let position = self.encase_box(inner_box_index, gene, fit_space);

            if to_pack.min_dim <= min_dim || to_pack.volume <= min_volume {
                (min_dim, min_volume) = self.min_dim_vol(&bps[box_position_strategy_index + 1..])
            }

            self.bins.bins[fit_bin].allocate(&position, |new_space| {
                new_space.min_dim() >= min_dim && new_space.volume() >= min_volume
            });

            positions.push(Position::new(position, fit_bin, inner_box_index));
        }

        let bins = self.bins.opened();
        let mut least_loads = bins.iter().map(|bin| bin.used_volume).collect::<Vec<f32>>();
        least_loads.sort_unstable_by(|a, b| a.partial_cmp(b).unwrap());
        let least_load = least_loads[0];
        (least_load, positions)
    }

    fn encase_box(&self, inner_box_index: usize, gene: &Vec<f32>, container: &Space) -> Space {
        let cuboid = &self.boxes[inner_box_index].cuboid;
        let gene = gene[gene.len() / 2 + inner_box_index];

        let mut orients = self.orient.borrow_mut();
        orients.clear();
        rotate(cuboid, orients.as_mut());
        orients.retain(|c| c.fits(container));

        let transcoded_gene = (gene * orients.len() as f32).ceil() as usize;
        let orientation = &orients[(transcoded_gene).max(1) - 1];
        Space::from_pos(container.origin(), orientation)
    }

    #[inline]
    fn min_dim_vol(&self, remain_bps: &[usize]) -> (f32, f32) {
        let (mut min_d, mut min_v) = (f32::MAX, f32::MAX);
        for &box_idx in remain_bps {
            let b = &self.boxes[box_idx];
            min_d = min_d.min(b.min_dim);
            min_v = min_v.min(b.volume);
        }
        (min_d, min_v)
    }
}

#[derive(Clone)]
struct BinList {
    cuboid_param: Cuboid,
    bins: Vec<Bin>,
}

impl BinList {
    fn new(cuboid_param: Cuboid) -> Self {
        BinList {
            cuboid_param,
            bins: Vec::new(),
        }
    }

    fn opened(&self) -> &[Bin] {
        &self.bins
    }

    fn create_bin(&mut self) -> usize {
        self.bins.push(Bin::new(self.cuboid_param));
        self.bins.len() - 1
    }

    fn reset(&mut self) {
        self.bins.clear();
    }
}
