/*
 * DuyDuc94
 */

import javax.swing.*;
import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.util.Scanner;

/**
 *
 * @author duy20
 */
public class GUI_Main extends JFrame {

    public static final Font FONT = new Font("Arial", Font.PLAIN, 20);
    public static final Scanner SC = new Scanner(System.in);
    private final JPanel ButtonPanel = new JPanel();
    private final JPanel OutputPanel = new JPanel();
    private final JTextArea OutputTextArea = new JTextArea();
    private final JPanel MainPanel = new JPanel();
    private final int NumberOfButtons = 7;
    private final JButton[] buttons = new JButton[NumberOfButtons];
    Core_IODataFile iof = new Core_IODataFile();
    Core_ProcessData pt = new Core_ProcessData();
    
    String function0 = "Open RawData.txt";
    String function1 = "Clear matrix and vector and group file";
    String function2 = "Read and write data";
    String function3 = "Change keyword";
    String fucntion4 = "Change region";
    String function5 = "Open Output folder";
    String function6 = "Show infomation";

    // CREATE buttonPanel
    public void initButtonPanel() {
        ButtonPanel.setLayout(new GridLayout(NumberOfButtons, 1)); // Algin vertical, n rows và 1 col
        //Declare buttons
        buttons[0] = new JButton(function0);
        buttons[1] = new JButton(function1);
        buttons[2] = new JButton(function2);
        buttons[3] = new JButton(function3);
        buttons[4] = new JButton(fucntion4);
        buttons[5] = new JButton(function5);
        buttons[6] = new JButton(function6);
        //Initialize properties of button
        for (JButton button : buttons) {
            //Add action listerner buttons
            button.addActionListener(new ButtonClickListener());
            //Add buttons into buttonPanel 
            ButtonPanel.add(button);
            //Set FONT for buttons
            button.setFont(FONT);
        }
    }

    // CREATE outputPanel
    public void initOutputPanel() {
        OutputPanel.setLayout(new BorderLayout());
        OutputTextArea.setFont(FONT);
        OutputTextArea.setEditable(false);          //Disable for edit in output
        OutputTextArea.setLineWrap(true);           //Enable line wrapping
        OutputTextArea.setWrapStyleWord(true);      //Wrap at word boundaries

        JScrollPane scrollPane = new JScrollPane(OutputTextArea);
        OutputPanel.add(scrollPane, BorderLayout.CENTER);
    }

    // CREATE MainPanel contains ButtonPanel and OutputPanel
    public void initMainPanel() {
        MainPanel.setLayout(new GridLayout(1, 2));
        MainPanel.add(ButtonPanel);
        MainPanel.add(OutputPanel);
    }

    public void frameProgram() {
        setTitle("Worldquant collect themes");
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        setSize(1000, 500);
        add(MainPanel);
        setLocationRelativeTo(null); // Display frame at center of screen
        setVisible(true);
    }

    private class ButtonClickListener implements ActionListener {
        public void actionPerformed(ActionEvent event) {
            JButton source = (JButton) event.getSource();
            String buttonText = source.getText();
            String endLine = "***********************************************************\n";
            if (buttonText.equals(function0)) {
                OutputTextArea.append(iof.getRawDataPath());
                OutputTextArea.append(iof.openInWindows(iof.getRawDataPath()));
                OutputTextArea.append(endLine);
            }
            if (buttonText.equals(function1)) {
                OutputTextArea.append(iof.clearMatrixData());
                OutputTextArea.append(iof.clearVectorData());
                OutputTextArea.append(iof.clearGroupData());
                OutputTextArea.append(endLine);
            }
            if (buttonText.equals(function2)) {
                OutputTextArea.append(iof.clearBufferData());
                OutputTextArea.append(iof.readRawData(pt));
                OutputTextArea.append(iof.readBufferData(pt));
                OutputTextArea.append(endLine);
            }
            if (buttonText.equals(function3)) {
                UIManager.put("OptionPane.messageFont", FONT);
                String input = JOptionPane.showInputDialog(GUI_Main.this,
                        "Input keyword: ");
                if (input != null) {
                    OutputTextArea.append("KEYWORD: " + pt.inputKeyword(input));
                    OutputTextArea.append("TYPE: " + Core_ProcessData.getTypes());
                    OutputTextArea.append(endLine);
                }
            }
            if (buttonText.equals(fucntion4)) {
                UIManager.put("OptionPane.messageFont", FONT);
                String input = JOptionPane.showInputDialog(GUI_Main.this,
                        "Current region is " + iof.getRegion() + ", input region:");
                if (input != null) {
                    OutputTextArea.append(iof.switchRegion(input));
                    OutputTextArea.append(endLine);
                }
            }
            if (buttonText.equals(function5)) {
                OutputTextArea.append(iof.openInWindows(iof.getOutputPath()));
                OutputTextArea.append(endLine);
            }
            if (buttonText.equals(function6)) {
                OutputTextArea.append(iof.showInfomation());
                OutputTextArea.append(endLine);
            }
        }
    }

    public static void main(String[] args) {
        SwingUtilities.invokeLater(() -> {
            GUI_Main program = new GUI_Main();
            program.initButtonPanel();
            program.initOutputPanel();
            program.initMainPanel();
            program.frameProgram();
        });
    }

}
