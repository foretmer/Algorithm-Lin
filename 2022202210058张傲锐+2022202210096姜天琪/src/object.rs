use serde::*;

#[derive(Copy, Clone, Debug, Serialize, Deserialize)]
pub struct Point {
    pub x: f32,
    pub y: f32,
    pub z: f32,
}

impl Point {
    pub fn new(x: f32, y: f32, z: f32) -> Self {
        Point { x, y, z }
    }

    #[inline(always)]
    pub fn distance(&self, other: &Self) -> f32 {
        let dx = self.x - other.x;
        let dy = self.y - other.y;
        let dz = self.z - other.z;
        dx * dx + dy * dy + dz * dz
    }

    #[inline(always)]
    fn less_than(&self, other: &Self) -> bool {
        self.x <= other.x && self.y <= other.y && self.z <= other.z
    }

    #[inline(always)]
    fn min(&self, other: &Self) -> Point {
        let x = self.x.min(other.x);
        let y = self.y.min(other.y);
        let z = self.z.min(other.z);
        Point::new(x, y, z)
    }

    #[inline(always)]
    fn max(&self, other: &Self) -> Point {
        let x = self.x.max(other.x);
        let y = self.y.max(other.y);
        let z = self.z.max(other.z);
        Point::new(x, y, z)
    }
}

impl PartialEq for Point {
    fn eq(&self, other: &Self) -> bool {
        self.x == other.x && self.y == other.y && self.z == other.z
    }

    fn ne(&self, other: &Self) -> bool {
        self.x != other.x || self.y != other.y || self.z != other.z
    }
}

#[derive(PartialEq, Copy, Clone, Debug, Serialize, Deserialize)]
pub struct Cuboid {
    pub length: f32,
    pub depth: f32,
    pub width: f32,
}

impl Cuboid {
    pub fn new(length: f32, depth: f32, width: f32) -> Self {
        Cuboid {
            length,
            depth,
            width,
        }
    }

    #[inline(always)]
    pub fn volume(&self) -> f32 {
        self.length * self.depth * self.width
    }

    #[inline(always)]
    pub fn fits(&self, space: &Space) -> bool {
        space.length() >= self.length && space.width() >= self.width && space.depth() >= self.depth
    }
}

impl Into<Cuboid> for &Cuboid {
    fn into(self) -> Cuboid {
        *self
    }
}

#[derive(Copy, Clone, Debug, Serialize, Deserialize)]
pub struct Space {
    pub min_corner: Point,
    pub max_corner: Point,
}

impl Space {
    #[inline(always)]
    pub fn new(min_corner: Point, max_corner: Point) -> Self {
        Space {
            min_corner,
            max_corner,
        }
    }

    #[inline(always)]
    pub fn from_pos(origin: &Point, rect: &Cuboid) -> Self {
        let x = origin.x + rect.length;
        let y = origin.y + rect.width;
        let z = origin.z + rect.depth;

        Space {
            min_corner: *origin,
            max_corner: Point::new(x, y, z),
        }
    }

    #[inline(always)]
    pub fn min_dim(&self) -> f32 {
        self.length().min(self.depth()).min(self.width())
    }

    #[inline(always)]
    pub fn origin(&self) -> &Point {
        &self.min_corner
    }

    #[inline(always)]
    pub fn length(&self) -> f32 {
        self.max_corner.x - self.min_corner.x
    }

    #[inline(always)]
    pub fn depth(&self) -> f32 {
        self.max_corner.z - self.min_corner.z
    }

    #[inline(always)]
    pub fn width(&self) -> f32 {
        self.max_corner.y - self.min_corner.y
    }

    #[inline(always)]
    pub fn contains(&self, other: &Self) -> bool {
        self.min_corner.less_than(&other.min_corner) && other.max_corner.less_than(&self.max_corner)
    }

    #[inline(always)]
    pub fn intersects(&self, other: &Self) -> bool {
        self.min_corner.less_than(&other.max_corner) && other.min_corner.less_than(&self.max_corner)
    }

    #[inline(always)]
    pub fn inter_area(&self, other: &Self) -> Self {
        let min_corner = self.min_corner.max(&other.min_corner);
        let max_corner = self.max_corner.min(&other.max_corner);
        Space::new(min_corner, max_corner)
    }

    #[inline(always)]
    pub fn volume(&self) -> f32 {
        self.length() * self.width() * self.depth()
    }
}

impl PartialEq for Space {
    fn eq(&self, other: &Self) -> bool {
        self.min_corner == other.min_corner && self.max_corner == other.max_corner
    }

    fn ne(&self, other: &Self) -> bool {
        self.min_corner != other.min_corner || self.max_corner != other.max_corner
    }
}
