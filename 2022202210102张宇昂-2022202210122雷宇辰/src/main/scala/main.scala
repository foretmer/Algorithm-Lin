package test.pack

import java.io.{BufferedWriter, FileWriter}
import scala.collection.mutable
import scala.collection.mutable.ArrayBuffer
import scala.io.Source
import scala.util.Random
import scala.util.control.Breaks.{break, breakable}

case class Point(x: Int, y: Int, z: Int)

enum Orientation:
  case TALL_WIDE, TALL_THIN, MID_WIDE, MID_THIN, SHORT_WIDE, SHORT_THIN

class Box(val dim1: Int, val dim2: Int, val dim3: Int) extends Cloneable:
  private val edges: Vector[Int] = Vector(dim1, dim2, dim3).sorted
  val volume: Int = edges.product
  var orientation: Orientation = Orientation.TALL_THIN
  var coord: Point = Point(-1, -1, -1)
  private val allShapes: Map[Orientation, Vector[Int]] =
    Map[Orientation, Vector[Int]](
      Orientation.TALL_THIN -> Vector(edges(1), edges(0), edges(2)),
      Orientation.TALL_WIDE -> Vector(edges(0), edges(1), edges(2)),
      Orientation.MID_THIN -> Vector(edges(2), edges(0), edges(1)),
      Orientation.MID_WIDE -> Vector(edges(0), edges(2), edges(1)),
      Orientation.SHORT_THIN -> Vector(edges(2), edges(1), edges(0)),
      Orientation.SHORT_WIDE -> Vector(edges(1), edges(2), edges(0)),
    )

  private def shape: Vector[Int] = allShapes(orientation)

  def length: Int = shape(0)

  def width: Int = shape(1)

  def height: Int = shape(2)

  def shadow(planar: String): Vector[Int] =
    planar match
      case "xy" => Vector(coord.x, coord.y, coord.x + shape(0), coord.y + shape(1))
      case "xz" => Vector(coord.x, coord.z, coord.x + shape(0), coord.z + shape(2))
      case "yz" => Vector(coord.y, coord.z, coord.y + shape(1), coord.z + shape(2))

  override def clone(): Box =
    val cloned = Box(dim1, dim2, dim3)
    cloned.coord = coord
    cloned.orientation = orientation
    cloned


def isShadowOverlap(rect1: Vector[Int], rect2: Vector[Int]): Boolean =
  val notOverlap = rect1(0) >= rect2(2) || rect1(1) >= rect2(3) ||
    rect2(0) >= rect1(2) || rect2(1) >= rect1(3)
  !notOverlap

def isBoxOverlap(box1: Box, box2: Box): Boolean =
  isShadowOverlap(box1.shadow("xy"), box2.shadow("xy")) &&
    isShadowOverlap(box1.shadow("yz"), box2.shadow("yz")) &&
    isShadowOverlap(box1.shadow("xz"), box2.shadow("xz"))

class Container(val length: Int, val width: Int, val height: Int):
  private val shape: Vector[Int] = Vector(length, width, height)
  val volume: Int = shape.product
  private var href = 0
  private var vref = 0
  private val availablePoints = mutable.TreeSet(Point(0, 0, 0))(using Ordering.by(p => (p.y, p.x, p.z)))
  private val packedBox = ArrayBuffer[Box]()

  private def canPack(pos: Point, box: Box): Boolean =
    val oriens = Orientation.values
    var flag = true
    breakable {
      for ori <- oriens do
        box.orientation = ori
        flag = true
        if pos.x + box.length > length || pos.y + box.width > width || pos.z + box.height > height then flag = false
        for b <- packedBox do
          box.coord = pos
          if isBoxOverlap(box, b) then flag = false
        if flag then break
    }
    flag

  private def moveBoxCoord(box: Box): Point =
    val xyz = ArrayBuffer(box.coord.x, box.coord.y, box.coord.z)
    for i <- 0 to 2 do
      var flag = true
      while xyz(i) > 1 && flag do
        xyz(i) -= 1
        box.coord = Point(xyz(0), xyz(1), xyz(2))
        breakable {
          for b <- packedBox do
            if isBoxOverlap(b, box) then
              xyz(i) += 1
              flag = false
              break
        }
    Point(xyz(0), xyz(1), xyz(2))

  def packBoxSeq(boxes: Vector[Box]): ArrayBuffer[Box] =
    var i = 0
    while i < boxes.size do
      val box = boxes(i)
      var flag = false
      var curPoint = Point(-1, -1, -1)

      breakable {
        for p <- availablePoints do
          if canPack(p, box) && p.x + box.length <= href && p.z + box.height <= vref then
            curPoint = p
            flag = true
            break
      }

      if !flag then
        if href == 0 || href == length then
          if canPack(Point(0, 0, vref), box) then
            curPoint = Point(0, 0, vref)
            flag = true
            vref += box.height
            href = box.length
          else if vref < height then
            vref = height
            href = length
            i -= 1
        else
          breakable {
            for
              p <- availablePoints
              if p.x == href
              if p.y == 0
            do
              if canPack(p, box) && p.z + box.height <= vref then
                curPoint = p
                flag = true
                href += box.length
                break
          }
          if !flag then
            href = length
            i -= 1

      if flag then
        box.coord = curPoint
        availablePoints -= curPoint

        box.coord = moveBoxCoord(box)
        packedBox += box
        availablePoints += Point(box.coord.x + box.length, box.coord.y, box.coord.z)
        availablePoints += Point(box.coord.x, box.coord.y + box.width, box.coord.z)
        availablePoints += Point(box.coord.x, box.coord.y, box.coord.z + box.height)

      i += 1
    packedBox


def packBoxSA(boxes: Vector[Box], l: Int, w: Int, h: Int, st: Double, et: Double, dt: Double): (ArrayBuffer[Box], Double) =
  val v = l * w * h
  var bbest = boxes
  var packedBox = ArrayBuffer.from(for cb <- Container(l, w, h).packBoxSeq(boxes) yield cb.clone())
  var fbest = computePackRatio(packedBox, v)
  var b = bbest
  var f = fbest
  var t = st
  while t >= et do
    val tmp1 = Random.between(0, boxes.size)
    val tmp2 = Random.between(0, boxes.size)
    val idx1 = Math.min(tmp1, tmp2)
    val idx2 = Math.max(tmp1, tmp2)
    val newSeq =
      val (s1, s2) = b.splitAt(idx2)
      val (s3, s4) = s1.splitAt(idx1)
      s3 ++ s4.reverse ++ s2

    val pb2 = Container(l, w, h).packBoxSeq(newSeq)
    val f2 = computePackRatio(pb2, v)
    val df = f2 - f
    if df > 0 then
      f = f2
      b = newSeq
      if f > fbest then
        fbest = f
        bbest = b
        packedBox = ArrayBuffer.from(for cb <- pb2 yield cb.clone())
    else
      val x = Random.nextDouble()
      if x < Math.exp(10 * df / t) then
        f = f2
        b = newSeq
    t *= dt

  (packedBox, fbest)

def computePackRatio(boxes: Iterable[Box], volume: Double): Double =
  boxes.map(_.volume).sum / volume

def readTests(filename: String): Vector[Vector[Box]] =
  val fp = Source.fromFile(filename)
  val jsonString = fp.getLines().mkString
  fp.close

  var ret: Vector[Vector[Box]] = Vector()
  val data = ujson.read(jsonString).arr
  for sample <- data do
    var boxes = Vector[Box]()
    for b <- sample.arr do
      boxes = boxes.appendedAll(for _ <- 1 to b(3).num.toInt yield Box(b(0).num.toInt, b(1).num.toInt, b(2).num.toInt))
    ret = ret.appended(boxes)

  ret

def writeResult(filename: String, packedBox: Iterable[Box], ratio: Double): Unit =
  val fp = BufferedWriter(FileWriter(filename))
  fp.write(ratio.toString)
  fp.newLine()
  fp.write("index,x,y,z,length,width,height")
  fp.newLine()
  var i = 1
  for box <- packedBox do
    fp.write(s"${i.toString},${box.coord.x},${box.coord.y},${box.coord.z},${box.length},${box.width},${box.height}")
    fp.newLine()
    i += 1

  fp.close()

def testRandom(test: Vector[Box], name: String): Unit =
  val boxes = Random.shuffle(test)
//  val boxes = test.sortBy(b => b.volume)(using Ordering.Int.reverse)
  val container = Container(587, 233, 220)
  val b = container.packBoxSeq(boxes)
  val ratio = computePackRatio(b, container.volume)
  writeResult(s"$name-random.csv", b, ratio)

def testSA(test: Vector[Box], name: String): Unit =
  val boxes = test.sortBy(b => b.volume)(using Ordering.Int.reverse)
  val (b, ratio) = packBoxSA(boxes, 587, 233, 220, 1.0, 0.1, 0.8)
  writeResult(s"$name-sa.csv", b, ratio)

@main
def main(): Unit =
  val tests = readTests("data.json")
  println(s"${tests.size} tests")
  for
    i <- 0 to 4
    j <- 0 to 4
  do
    val name = s"E${i + 1}-${j + 1}"
    println(name)
    testRandom(tests(i * 5 + j), name)
    testSA(tests(i * 5 + j), name)
