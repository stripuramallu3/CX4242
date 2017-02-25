package edu.gatech.cse6242;
import java.io.IOException;
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

public class Task1 {
	public static class TokenizerMapper extends Mapper<Object, Text, Text, IntWritable>{
    	private Text txt = new Text();
		public void map(Object key, Text value, Context context) throws IOException, InterruptedException {
		   StringTokenizer itr = new StringTokenizer(value.toString(), "\t");
		   itr.nextToken();
		   txt.set(itr.nextToken());
		   String weight = itr.nextToken();
		   context.write(txt, new IntWritable(Integer.parseInt(weight)));
		}
	}
	public static class MaxReducer extends Reducer<Text, IntWritable, Text, IntWritable> {
		private IntWritable result = new IntWritable();
		public void reduce(Text key, Iterable<IntWritable> values, Context context) throws IOException, InterruptedException {
			int maxValue = 0;
			for (IntWritable val : values) {
				int tmp = val.get();
				if (tmp > maxValue) {
					maxValue = tmp;
				}
			}
			result.set(maxValue);
			context.write(key, result);
		}
	}
	public static void main(String[] args) throws Exception {
	    Configuration conf = new Configuration();
	    Job job = Job.getInstance(conf, "Task1");
	    job.setJarByClass(Task1.class);
	    job.setMapperClass(TokenizerMapper.class);
	    job.setCombinerClass(MaxReducer.class);
	    job.setReducerClass(MaxReducer.class);
	    job.setOutputKeyClass(Text.class);
	    job.setOutputValueClass(IntWritable.class);
	    job.setInputFormatClass(TextInputFormat.class);
	    job.setOutputFormatClass(TextOutputFormat.class);

	    FileInputFormat.addInputPath(job, new Path(args[0]));
	    FileOutputFormat.setOutputPath(job, new Path(args[1]));
	    System.exit(job.waitForCompletion(true) ? 0 : 1);
	}
}

