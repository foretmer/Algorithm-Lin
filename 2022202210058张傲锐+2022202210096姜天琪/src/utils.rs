use crate::object::{Cuboid, Point, Space};
use std::{cell::RefCell, sync::Arc};

#[derive(Clone)]
pub struct Bin {
    params: Cuboid,
    pub(crate) used_volume: f32,
    pub(crate) empty_list: Vec<Space>,
    intersects: Vec<usize>,
    empty_spaces: Vec<Space>,
    orients: Arc<RefCell<Vec<Cuboid>>>,
}

impl Bin {
    pub(crate) fn new(spec: Cuboid) -> Self {
        let empty_list = vec![Space::from_pos(&Point::new(0.0, 0.0, 0.0), &spec)];
        Bin {
            params: spec,
            empty_list,
            used_volume: 0.0,
            intersects: Vec::new(),
            empty_spaces: Vec::new(),
            orients: Arc::new(RefCell::new(Vec::with_capacity(6))),
        }
    }

    pub(crate) fn allocate<F>(&mut self, space: &Space, mut new_space_filter: F)
    where
        F: FnMut(&Space) -> bool,
    {
        self.used_volume += space.volume();

        self.intersects.clear();
        let spaces_intersects = self
            .empty_list
            .iter()
            .enumerate()
            .filter(|(_, ems)| ems.intersects(space))
            .map(|(i, _)| i);
        self.intersects.extend(spaces_intersects);

        self.empty_spaces.clear();
        for &i in self.intersects.iter() {
            let ems = &self.empty_list[i];
            let inter = ems.inter_area(space);
            find_new_space(ems, &inter, &mut self.empty_spaces, |s| new_space_filter(s))
        }

        for &i in self.intersects.iter().rev() {
            self.empty_list.remove(i);
        }
        self.empty_list.retain(|s| new_space_filter(s));

        self.empty_list
            .extend(self.empty_spaces.iter().filter(|&s| {
                !self
                    .empty_spaces
                    .iter()
                    .any(|other| other != s && other.contains(s))
            }))
    }

    pub(crate) fn try_encase(&self, cuboid: &Cuboid) -> Option<&Space> {
        let mut max_dist = -1.0;
        let mut best_ems = None;
        let mut orients = self.orients.borrow_mut();

        orients.clear();
        rotate(cuboid, orients.as_mut());
        let container_max_corner =
            Point::new(self.params.length, self.params.depth, self.params.width);

        for ems in &self.empty_list {
            if ems.volume() >= cuboid.volume() {
                let fits_orient = orients
                    .iter()
                    .find(|o| o.fits(ems))
                    .map(|o| Space::from_pos(ems.origin(), o));

                if let Some(o) = fits_orient {
                    let box_max_corner = o.max_corner;
                    let dist = container_max_corner.distance(&box_max_corner);
                    if dist > max_dist {
                        max_dist = dist;
                        best_ems = Some(ems);
                    }
                }
            }
        }
        best_ems
    }
}

#[inline]
fn find_new_space<F>(
    this: &Space,
    other: &Space,
    new_spaces: &mut Vec<Space>,
    mut new_space_filter: F,
) where
    F: FnMut(&Space) -> bool,
{
    let (tmin, tmax, omin, omax) = (
        this.min_corner,
        this.max_corner,
        other.min_corner,
        other.max_corner,
    );
    for &(a, b) in &[
        (tmin, Point::new(omin.x, tmax.y, tmax.z)),
        (Point::new(omax.x, tmin.y, tmin.z), tmax),
        (tmin, Point::new(tmax.x, omin.y, tmax.z)),
        (Point::new(tmin.x, omax.y, tmin.z), tmax),
        (tmin, Point::new(tmax.x, tmax.y, omin.z)),
        (Point::new(tmin.x, tmin.y, omax.z), tmax),
    ] {
        let space = Space::new(a, b);
        if space.length().min(space.depth()).min(space.width()) > 0e-5 && new_space_filter(&space) {
            new_spaces.push(space);
        }
    }
}

pub fn rotate(cuboid: &Cuboid, orient: &mut Vec<Cuboid>) {
    let sides = [cuboid.length, cuboid.width, cuboid.depth];
    for (i, &l) in sides.iter().enumerate() {
        for (j, &w) in sides.iter().enumerate() {
            if i == j {
                continue;
            }
            for (k, &d) in sides.iter().enumerate() {
                if i == k || j == k {
                    continue;
                }
                orient.push(Cuboid::new(l, w, d));
            }
        }
    }
}

#[derive(Clone, Copy, Debug)]
pub struct Position {
    pub space: Space,
    pub bin_no: usize,
    pub box_idx: usize,
}

impl Position {
    pub(crate) fn new(space: Space, bin_no: usize, box_idx: usize) -> Self {
        Position {
            space,
            bin_no,
            box_idx,
        }
    }
}

#[derive(Debug, Clone)]
pub struct Box {
    pub cuboid: Cuboid,
    pub min_dim: f32,
    pub volume: f32,
}

impl<T> From<T> for Box
where
    T: Into<Cuboid>,
{
    fn from(raw: T) -> Self {
        let cuboid = raw.into();
        let min_dim = cuboid.width.min(cuboid.length).min(cuboid.depth);
        let volume = cuboid.volume();
        Box {
            cuboid,
            min_dim,
            volume,
        }
    }
}
