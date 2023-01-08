#![feature(drain_filter)]

use std::fs::File;
use std::io::prelude::*;
use std::iter;
use std::path::Path;
use std::thread;
use std::time::Instant;

use csv;
use serde::*;

use crate::ga::{EvolutionaryAlgorithm, Params, RandGenerator};
use crate::object::{Cuboid, Space};
use crate::solver::Transcoder;

pub mod object;

mod ga;
mod utils;
mod solver;

fn main() {
    let start = Instant::now();

    let items = load_items("testdata/data.csv");
    let bin = Cuboid::new(587.0, 233.0, 220.0);
    let bins = pack_boxes(bin, &items);
    let elapsed = start.elapsed();
    println!("Elapsed time: {} milliseconds", elapsed.as_millis());
    // println!("{:?}", bins);
    let bin_clone = bin.clone();
    let bins_clone = bins.clone();
    let handler = thread::spawn(move || {
        let v = bin_clone.volume();
        let mut sum_v = 0.0;
        for package in bins_clone {
            sum_v += package.volume();
        }
        println!("{:?}", sum_v as f32 / v as f32);
    });

    // println!("{:?}", bins);
    let path = "./test.txt";
    let mut f = File::create(path).unwrap();
    let b = format!("{} {} {}\n", bin.length, bin.width, bin.depth);

    f.write(b.as_bytes()).unwrap();
    for position in bins.clone() {
        let space = position;
        let cuboid = format!(
            "{} {} {} {} {} {}\n",
            space.min_corner.x,
            space.min_corner.y,
            space.min_corner.z,
            space.length(),
            space.width(),
            space.depth()
        );

        f.write(cuboid.as_bytes()).unwrap();
    }
    handler.join().unwrap();
}

pub fn pack_boxes<'a, T>(bin_spec: Cuboid, boxes: &'a [T]) -> Vec<Space>
    where
        T: Sync,
        &'a T: Into<Cuboid>,
{
    let generator = RandGenerator::new(boxes.len() * 2);
    let mut params = Params::default();
    params.get_params(boxes.len());
    let mut solver =
        EvolutionaryAlgorithm::new(params, generator, || Transcoder::new(boxes, bin_spec));
    let solution = solver.solve();
    let mut bins = Vec::new();
    for inner_position in &solution.1 {
        let idx = inner_position.bin_no;
        if idx != 0 {
            continue;
        }
        let space = inner_position.space;
        bins.push(space)
    }
    bins
}

#[derive(Debug, Deserialize)]
struct Record {
    width: f32,
    depth: f32,
    height: f32,
    count: usize,
}

pub fn load_items<P: AsRef<Path>>(path: P) -> Vec<Cuboid> {
    let mut rdr = csv::Reader::from_path(path).unwrap();
    let mut v = Vec::new();
    for record in rdr.deserialize() {
        let record: Record = record.unwrap();
        v.extend(
            iter::repeat(Cuboid::new(record.width, record.depth, record.height)).take(record.count),
        );
    }
    v
}
