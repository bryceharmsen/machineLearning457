package app;

import weka.core.Instances;
import weka.core.Debug.Random;
import weka.core.converters.ConverterUtils.DataSource;

import java.io.File;
import java.io.FileWriter;
import java.io.IOException;
import java.util.ArrayList;
import java.util.Arrays;
import java.util.Iterator;

import weka.classifiers.Evaluation;
import weka.classifiers.functions.MultilayerPerceptron;

public class App {
    private final String SAMPLES_PATH = "../../data/";
    private final String TRAIN_SAMPLES_FILE = SAMPLES_PATH + "trainSamples.arff";
    private final String TEST_SAMPLES_FILE = SAMPLES_PATH + "testSamples.arff";

    public double executeTrial(String[] options, String fileName) throws Exception, IOException {
        System.out.println(fileName);
        File resultsFile = new File("../../results/" + fileName + ".txt");

        FileWriter writer = new FileWriter(resultsFile);

        DataSource trainSource = new DataSource(this.TRAIN_SAMPLES_FILE),
                testSource = new DataSource(this.TEST_SAMPLES_FILE);
        Instances trainData = trainSource.getDataSet(),
                testData = testSource.getDataSet();
        writer.write(
        trainData.numInstances() + " training instances loaded.\n" +
        testData.numInstances() + " testing instances loaded.\n"
        );
        trainData.setClassIndex(trainData.numAttributes() - 1);
        testData.setClassIndex(testData.numAttributes() - 1);

        MultilayerPerceptron mlp = new MultilayerPerceptron();
        mlp.setOptions(options);
        mlp.buildClassifier(trainData);
        writer.write(mlp.toString());
        mlp.setGUI(true);

        Evaluation eval = new Evaluation(trainData);
        eval.evaluateModel(mlp, testData);
        writer.write(eval.toSummaryString("Results\n", false));
        writer.close();

        return eval.correlationCoefficient();
    }

    public String[] getNeuronConfigurations(int loNeuron, int hiNeuron, int loLayers, int hiLayers) {
        ArrayList<String> configs = new ArrayList<>();
        Random rand = new Random();
        Iterator<Integer> ints = rand.ints(loNeuron, hiNeuron + 1).iterator();
        for (int i = loLayers; i <= hiLayers; i++) {
            for (int j = loNeuron; j <= hiNeuron; j++) {
                StringBuilder str = new StringBuilder();
                for (int k = 0; k < i; k++) {
                    str.append(ints.next());
                    if (k < i - 1) str.append(",");
                }
                configs.add(str.toString());
            }
        }
        return configs.toArray(new String[0]);
    }

    public void run() throws Exception {
        try {
            String[] options = {
                "-L", "0.3", "-M", "0.2",
                "-N", "500", "-V", "0", 
                "-S", "0", "-E", "20", 
                "-H", "1"
            };
            int minNeuron = 0, maxNeuron = 19,
                minLayer = 1, maxLayer = 2;
            String[] configs = this.getNeuronConfigurations(minNeuron, maxNeuron, minLayer, maxLayer);
            double bestCorrelation = 0;
            String bestFileName = "";
            for (String config : configs) {
                options[options.length - 1] = config;
                String fileName = config.replace(",", "");
                double correlation = 0;
                try {
                    correlation = this.executeTrial(Arrays.copyOf(options, options.length), fileName);
                } catch (IOException ioe) {
                    System.out.println("Already tried config " + config + ", moving on.");
                    continue;
                }
                if (correlation > bestCorrelation) {
                    bestCorrelation = correlation;
                    bestFileName = fileName;
                }
            }
            System.out.println("Best results: " + bestFileName + ".");
        } catch (Exception e) {
            System.out.println(e.getMessage());
            System.out.println(e.getStackTrace()); 
        }
    }

    public static void main(String[] args) throws Exception {
        //run with 'java -cp "/usr/share/java/weka.jar" App.java'
        App mlp = new App();
        mlp.run();
    }
}