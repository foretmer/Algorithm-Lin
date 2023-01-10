from pack import Packer
from box import Box
from space_holder import Holder
from container import Container
from coordinate import Coordinate

import copy
import random
import functools
# partially matching cross-over
# Simple Inversion Mutation


class Gene():
    def __init__(self, box: Box, orientation: int):
        self.box = box
        self.orientation = orientation
    
    @staticmethod
    def cmp_floorspace(a, b):
        if a.box.get_floor_space() < b.box.get_floor_space():
            return 1
        elif a.box.get_floor_space() > b.box.get_floor_space():
            return -1
        return 0
    
    # To make up the absence of the mutaion of orientation
    def mutate(self):
        self.orientation = (self.orientation+1)%2

class Genome():
    #pattern, a ordering list that can build a ordering scheme
    def __init__(self):
        self.pattern = []
    def get_mutate(self, mutaion_probability):
        
        mutated_genome = copy.deepcopy(self)
        mutated_genome.pattern = mutated_genome.pattern
        genome_length = len(mutated_genome.pattern)

        for gene in mutated_genome.pattern:
            if random.random() <= mutaion_probability:
                gene.mutate()
        return mutated_genome


class GeneticPacker(Packer):

    def __init__(self, container: Container,  limited_population_size: int, mutaion_probability:float, times: int):
        self.box_list = None
        self.population = None
        self.limited_population_size = limited_population_size
        self.mutaion_probability = mutaion_probability
        self.stage_best_fitness=[]
        self.stage_best_scheme=[]
        self.containers = []
        self.time = times
        Packer.__init__(self, container)
    
    # get the packing scheme
    def get_scheme(self, boxes):
        self.box_list = sorted(boxes, key=functools.cmp_to_key(Box.cmp_floorspace), reverse = False)
        self.execute(self.time)
        best_pos = 0
        best_fit = 0
        for n in range(len(self.stage_best_fitness)):
            if self.stage_best_fitness[n] > best_fit:
                best_pos = n
                best_fit = self.stage_best_fitness[best_pos]
        best_fit = self.stage_best_fitness[best_pos]
        best_scheme = self.stage_best_scheme[best_pos]
        best_container_list = self.containers[best_pos]
        return (best_fit, best_container_list, best_scheme)

    # process control of the genetic algorithm
    def execute(self, time:int):
        print(f'random init')
        self.population = self.random_init_process(self.limited_population_size)
        for n in range(time):
            print(f'the {n} turn...')
            print('selection begin')
            self.selection_process(self.population)
            print(f'max fitness {self.stage_best_fitness[n]}')

            if len(self.population) ==0:
                return []
            print('crossover begin')
            self.crossover_process(self.population)
            print('mutation begin')
            self.mutation_process(self.population)
            print(f'end, population size {len(self.population)}')

    #########

    ### from now on are the partial processes function
    ###

    # random init
    # param: num --the population size
    def random_init_process(self, num: int):
        
        population=[]
        if num <= 0:
            return population
        for n in range(num):
            population.append(self.random_generate())
        return population
   
    # selection
    # pram: population --the population
    def selection_process(self, population):
        if len(population) ==0:
            return []
        fitness_list = {}
        selected_population = []

        for individual in population:
            the_fit = self.get_fitness(individual)
            fitness_list[individual] = the_fit

        # sort and select
        ordered_list = sorted(fitness_list.items(), key=lambda x:x[1], reverse=True)

        self.stage_best_fitness.append(ordered_list[1][1])
        the_scheme, the_container_list =  self.get_simulation(ordered_list[0][0])

        self.stage_best_scheme.append(the_scheme)
        self.containers.append(the_container_list)

        '''
        # this is a selection method that was not suitable
        # when there is no enough fitness individuals
            q = 1
            gamma = q/(1-(1-q)**self.limited_population_size)
            for i in range(len(ordered_list)):
                p = gamma*(1-q)**(i)
                if random.random() <= p:
                    selected_population.append(ordered_list[i][0])
        '''
        # select the better individuals of population
        selected_population.extend([ordered_list[i][0] for i in range(self.limited_population_size//100)])

        # 1. some times there could n't enough valid individual as for limited limited_population_size and
        #    which is limited because of time and space complexity balancing
        #    the added process is to supplement the population
        # 2. this is also a process to generate random individuals to population
        #    so pupulation has two part [better individuals, new random individuals] 
        #    this is to keep both the ability of get optimal solution and speed
        new_gener = self.random_init_process(self.limited_population_size//100)
        selected_population.extend(new_gener)

        population.clear()
        population.extend(selected_population)
        return selected_population


    def mutation_process(self, population):
        mutated_population = []
        for individual in population:
            mutated_population.append(individual.get_mutate(self.mutaion_probability))
        population.extend(mutated_population)
        return population

    def crossover_process(self, population):
        next_generation = []
        for father in population:
            for mother in population:
                next_generation.extend(self.get_child(father, mother))
                
        population.extend(next_generation)
    ###                     
    ### process function end###

    ### from now on are the suportted functions    
    ###
    def get_child(self, genome_a: Genome, genome_b: Genome):
        
        father = copy.deepcopy(genome_a)
        mother = copy.deepcopy(genome_b)
        self.crossover(father, mother)
        return [father,mother]
    def crossover(self, genome_a: Genome, genome_b: Genome):
        if len(genome_a.pattern)!= len(genome_b.pattern):
            print(f'1 a {len(genome_a.pattern)} b {len(genome_b.pattern)}')
            input()
        genome_length = len(genome_a.pattern)
        begin_pos = random.choice(range(genome_length))
        end_pos = random.choice(range(genome_length))
        begin_pos, end_pos = ((begin_pos, end_pos) if(begin_pos< end_pos) else (end_pos, begin_pos))
        
        a_map_to_b = {}
        b_map_to_a = {}
        for i in range(begin_pos, end_pos):
            if genome_a.pattern[i] != genome_b.pattern[i] :
                a_map_to_b[genome_a.pattern[i]] = genome_b.pattern[i].orientation
                b_map_to_a[genome_b.pattern[i]] = genome_a.pattern[i].orientation
        for i in range (genome_length):
            if i in range(begin_pos, end_pos):
                genome_a.pattern[i], genome_b.pattern[i] = genome_b.pattern[i], genome_a.pattern[i]
            else:
                if genome_a.pattern[i] in b_map_to_a:
                    genome_a.pattern[i] = b_map_to_a[genome_a.pattern[i]].orientation
                if genome_b.pattern[i] in a_map_to_b:
                    genome_b.pattern[i] = a_map_to_b[genome_b.pattern[i]].orientation
        if len(genome_a.pattern)!= len(genome_b.pattern):
            print(f'2 a {len(genome_a.pattern)} b {len(genome_b.pattern)}')
            input()
        
    # return the fitness, from scheme, 
    def get_fitness(self, genome: Genome):
        holder_list, containers = self.get_simulation(genome)

        if len(holder_list) > 0:
            max_width = 0
            max_depth = 0
            max_height = 0
            used_volume = 0
            for each_holder in holder_list:
                width = each_holder.x + each_holder.get_width()
                depth = each_holder.y + each_holder.get_depth()
                height = each_holder.z + each_holder.get_height()
                max_width = (max_width if (max_width> width) else width)
                max_depth = (max_depth if (max_depth> depth) else depth)
                max_height = (max_height if (max_height> height) else height)
                used_volume = used_volume + each_holder.get_width()*each_holder.get_depth()*each_holder.get_height()
            volume = max_depth * max_height * max_width
            fitness = used_volume / volume
            return fitness
        else:
            return 0
 
    # return schema, a list of holder which contains each box's coordinate and orientation
    # from simulated built ordering scheme, get the utility
    def get_simulation(self,genome: Genome):
        unpacked_gene_list = list(genome.pattern)
        holder_list = []
        container_list = [self.container]
        while len(unpacked_gene_list) >0:
            selected_gene = unpacked_gene_list[0]

            candidate_holder = []
            for each_container in container_list:
                result = each_container.fit_orientation(selected_gene.box, selected_gene.orientation)
                if not result is None:
                    candidate_holder.append(result)
            if len(candidate_holder) <=0:
                break
                # return [], []
            else:
                candidate_holder.sort(key=functools.cmp_to_key(Coordinate.cmp_coordinate), reverse = True)
                # print(len(holder_list),candidate_holder)
                the_holder = candidate_holder.pop(0)
                remain_space = []
                
                for each_container in container_list:
                    if each_container.is_empty():
                        container_list.remove(each_container)
                for each_container in container_list:
                    if Coordinate.cmp_coordinate(each_container, the_holder) == 0:
                        remain_space.extend(each_container.get_free_space(the_holder))
                        container_list.remove(each_container)
                for each_container in container_list:
                    if each_container.is_empty():
                        container_list.remove(each_container)

                # merge space to increase the space utility
                for each_container in container_list:
                    for candidate_space in remain_space:
                        if Container.merge(each_container,candidate_space):
                            remain_space.remove(candidate_space)
                

                container_list.extend(remain_space)

                holder_list.append(the_holder)
                unpacked_gene_list.pop(0)


        return holder_list, container_list
      
    def random_generate(self):
        genome= Genome()
        boxes = list(self.box_list)
        pattern = [ Gene(box, random.choice(range(2)) ) for box in boxes]

        genome.pattern = pattern
        return genome
    ###
    ### suported function ends
