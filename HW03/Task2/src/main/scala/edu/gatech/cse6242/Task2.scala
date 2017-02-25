package edu.gatech.cse6242

import org.apache.spark.SparkContext
import org.apache.spark.SparkContext._
import org.apache.spark.SparkConf

object Task2 {
  def main(args: Array[String]) {
    val sc = new SparkContext(new SparkConf().setAppName("Task2"))

    // read the file
    val file = sc.textFile("hdfs://localhost:8020" + args(0))

    /* TODO: Needs to be implemented */
    //Isolate the tokens by tabs
    val tokenized = file.map(x => x.split("\t"))
    //Filter out all weights that are -1
    val filtered = tokenized.filter(x => x(2).toInt != 1)
    //Obatin all of the negative weights for each source/weight pair
    val src = filtered.map(x => (x(0),x(2).toInt * -1))
    //Obtain all of the positive weights for each target/weight pair
    val tgt = filtered.map(x => (x(1),x(2).toInt))
    //Union the src and tgt sets
    val merged = src.union(tgt)
    //Add the corresponding values for each key after eliminating duplicates
    val reduced = merged.reduceByKey(_+_)
    val file2 = reduced.map(x => Array(x._1.toString, x._2.toString).mkString("\t"))

    // store output on given HDFS path.
    // YOU NEED TO CHANGE THIS
    file2.saveAsTextFile("hdfs://localhost:8020" + args(1))
  }
}
