package edu.gatech.cse6242;

import java.io.*;
import java.util.StringTokenizer;
import org.apache.hadoop.fs.Path;
import org.apache.hadoop.conf.Configuration;
import org.apache.hadoop.io.*;
import org.apache.hadoop.mapreduce.*;
import org.apache.hadoop.util.*;
import org.apache.hadoop.mapreduce.lib.input.FileInputFormat;
import org.apache.hadoop.mapreduce.lib.input.TextInputFormat;
import org.apache.hadoop.mapreduce.lib.output.FileOutputFormat;
import org.apache.hadoop.mapreduce.lib.output.TextOutputFormat;
import org.apache.hadoop.fs.*;

public class Task4 {
    public static class TokenizerMapper1 extends Mapper<Object, Text, Text, IntWritable>{
        private Text node1 = new Text();
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
           StringTokenizer itr = new StringTokenizer(value.toString(), "\t");
           while (itr.hasMoreTokens()) {
            node1.set(itr.nextToken());
            context.write(node1, new IntWritable(1));
           }
        }
    }
    public static class MapReducer1 extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }
    public static class TokenizerMapper2 extends Mapper<Object, Text, Text, IntWritable>{
        private Text node1 = new Text();
        public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
           StringTokenizer itr = new StringTokenizer(value.toString(), "\t");
           itr.nextToken();
           node1.set(itr.nextToken());
           context.write(node1, new IntWritable(1));
        }
    }
    public static class MapReducer2 extends Reducer<Text, IntWritable, Text, IntWritable> {
        private IntWritable result = new IntWritable();
        public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
            int sum = 0;
            for (IntWritable val : values) {
                sum += val.get();
            }
            result.set(sum);
            context.write(key, result);
        }
    }

  public static void main(String[] args) throws Exception {
    Configuration conf = new Configuration();
    Job job = Job.getInstance(conf, "Task4");

    job.setJarByClass(Task4.class);
    job.setMapperClass(TokenizerMapper1.class);
    job.setCombinerClass(MapReducer1.class);
    job.setReducerClass(MapReducer1.class);
    job.setOutputKeyClass(Text.class);
    job.setOutputValueClass(IntWritable.class);
    job.setInputFormatClass(TextInputFormat.class);
    job.setOutputFormatClass(TextOutputFormat.class);

    FileInputFormat.addInputPath(job, new Path(args[0]));
    FileOutputFormat.setOutputPath(job, new Path("/user/cse6242/tempStep"));

    job.waitForCompletion(true);

    Configuration conf2 = new Configuration();
    Job job2 = Job.getInstance(conf2, "Task4");
    job2.setJarByClass(Task4.class);
    job2.setMapperClass(TokenizerMapper2.class);
    job2.setCombinerClass(MapReducer2.class);
    job2.setReducerClass(MapReducer2.class);
    job2.setOutputKeyClass(Text.class);
    job2.setOutputValueClass(IntWritable.class);
    job2.setInputFormatClass(TextInputFormat.class);
    job2.setOutputFormatClass(TextOutputFormat.class);

    FileInputFormat.addInputPath(job2, new Path("/user/cse6242/tempStep"));
    FileOutputFormat.setOutputPath(job2, new Path(args[1]));
	
    System.exit(job2.waitForCompletion(true) ? 0 : 1);

  }
}
