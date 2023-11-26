import javax.swing.*;
import javax.swing.event.TreeSelectionEvent;
import javax.swing.event.TreeSelectionListener;
import javax.swing.tree.DefaultTreeCellRenderer;
import javax.swing.tree.DefaultMutableTreeNode;
import javax.swing.tree.DefaultTreeModel;
import javax.swing.tree.TreeNode;
import javax.swing.tree.TreePath;

import java.awt.*;
import java.awt.event.ActionEvent;
import java.awt.event.ActionListener;
import java.awt.event.MouseAdapter;
import java.awt.event.MouseEvent;
import java.io.File;
import java.io.IOException;
import java.nio.file.Files;
import java.nio.file.Path;
import java.nio.file.Paths;
import java.util.ArrayList;
import java.util.Collections;
import java.util.Enumeration;

// FileNode 클래스는 파일 시스템의 파일을 나타냅니다.
class FileNode {
    private File file;

    public FileNode(File file) {
        this.file = file;
    }

    public File getFile() {
        return file;
    }

    public boolean isDirectory() {
        return file.isDirectory();
    }

    @Override
    public String toString() {
        return file.getName();
    }
}

// Regedit 클래스는 Swing 프레임을 확장하여 파일 시스템의 디렉토리 구조를 표시하고 편집하는 데 사용됩니다.
public class Regedit extends JFrame {

    private JTree directoryTree;
    private DefaultTreeModel treeModel;
    private JPanel rightPanel;

    private String regPath;
    private final String regRoot;

    // 생성자에서는 윈도우 설정, UI 구성 요소 초기화 및 이벤트 핸들러 설정이 이루어집니다.
    public Regedit(String path) {
        super("Helium Registry Editor");
        
        regPath = path;
        regRoot = path;
        FileNode rootFileNode = new FileNode(new File(regPath));
        DefaultMutableTreeNode root = new DefaultMutableTreeNode(rootFileNode);

        JTextField addressBar = new JTextField(File.separator);
        addressBar.addActionListener(new ActionListener() {
            @Override
            public void actionPerformed(ActionEvent e) {
                regPath = regRoot + (regRoot.endsWith(File.separator) ? "" : File.separator) + addressBar.getText();
                refreshTree();
                expandAll(directoryTree, new TreePath(treeModel.getRoot()));
            }
        });
        getContentPane().add(addressBar, BorderLayout.NORTH);

        treeModel = new DefaultTreeModel(root);
        directoryTree = new JTree(treeModel);
        directoryTree.setRootVisible(true);
        directoryTree.setShowsRootHandles(true);

         directoryTree.setCellRenderer(new DefaultTreeCellRenderer() {
            @Override
            public Component getTreeCellRendererComponent(JTree tree, Object value, boolean sel, boolean expanded, boolean leaf, int row, boolean hasFocus) {
                super.getTreeCellRendererComponent(tree, value, sel, expanded, leaf, row, hasFocus);
                // Use the open icon for all nodes
                setIcon(getOpenIcon());
                return this;
            }
        });

        directoryTree.addTreeSelectionListener(new TreeSelectionListener() {
            public void valueChanged(TreeSelectionEvent event) {
                DefaultMutableTreeNode node = (DefaultMutableTreeNode) directoryTree.getLastSelectedPathComponent();
                if (node == null) return;

                FileNode fileNode = (FileNode) node.getUserObject();
                if (fileNode.isDirectory()) {
                    rightPanel.removeAll();
                    File[] files = fileNode.getFile().listFiles();
                    ArrayList<File> fileList = new ArrayList<>();
                    if (files != null) {
                        for (File file : files) {
                            fileList.add(file);
                        }
                    }else{
                        return;
                    }
                    Collections.sort(fileList);
                    if (fileList != null) {
                        for (File file : fileList) {
                            if (!file.isDirectory() && !file.getName().startsWith(".")) {
                                JLabel fileLabel = new JLabel(file.getName());
                                fileLabel.addMouseListener(new MouseAdapter() {
                                    @Override
                                    public void mouseClicked(MouseEvent e) {
                                        openFileEditor(file.toPath());
                                    }
                                });
                                rightPanel.add(fileLabel);
                            }
                        }
                    }
                    rightPanel.revalidate();
                    rightPanel.repaint();
                    addressBar.setText(fileNode.getFile().getAbsolutePath().substring(new File(regRoot).getAbsolutePath().length()));
                }
            }
        });

        directoryTree.addMouseListener(new MouseAdapter() {
            @Override
            public void mouseClicked(MouseEvent e) {
                if (SwingUtilities.isRightMouseButton(e)) {
                    int row = directoryTree.getClosestRowForLocation(e.getX(), e.getY());
                    directoryTree.setSelectionRow(row);
                    DefaultMutableTreeNode node = (DefaultMutableTreeNode) directoryTree.getLastSelectedPathComponent();
                    if (node == null) return;

                    FileNode fileNode = (FileNode) node.getUserObject();
                    if (fileNode.isDirectory()) {
                        showPopup(e, node);
                    }
                }
            }
        });


        JScrollPane treeView = new JScrollPane(directoryTree);
        
        rightPanel = new JPanel();
        rightPanel.setLayout(new BoxLayout(rightPanel, BoxLayout.Y_AXIS));
        JScrollPane rightView = new JScrollPane(rightPanel);
        
        JSplitPane splitPane = new JSplitPane(JSplitPane.HORIZONTAL_SPLIT);
        splitPane.setLeftComponent(treeView);
        splitPane.setRightComponent(rightView);
        
        Dimension minimumSize = new Dimension(100, 50);
        rightView.setMinimumSize(minimumSize);
        treeView.setMinimumSize(minimumSize);
        splitPane.setDividerLocation(200); 
        splitPane.setPreferredSize(new Dimension(500, 300));

        getContentPane().add(splitPane);
        
        pack();
        setSize(800, 600);
        setVisible(true);
        setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);

        createChildren(rootFileNode, root);
    }

    private void openFileEditor(Path filePath) {
        try {
            String fileContent = Files.readString(filePath);
            JDialog dialog = new JDialog(this, "Edit File", true);
            dialog.setLayout(new BorderLayout());

            JLabel titleLabel = new JLabel(filePath.getFileName().toString());
            titleLabel.setHorizontalAlignment(JLabel.CENTER);
            dialog.add(titleLabel, BorderLayout.NORTH);

            JTextField textField = new JTextField(fileContent);
            textField.setBorder(BorderFactory.createCompoundBorder(
                    textField.getBorder(), 
                    BorderFactory.createEmptyBorder(5, 5, 5, 5)));
            dialog.add(textField, BorderLayout.CENTER);

            JPanel buttonPanel = new JPanel();
            buttonPanel.setBorder(BorderFactory.createEmptyBorder(5, 5, 5, 5));

            JButton saveButton = new JButton("Save");
            saveButton.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    try {
                        Files.writeString(filePath, textField.getText());
                        dialog.dispose();
                    } catch (IOException ex) {
                        JOptionPane.showMessageDialog(dialog, "Could not save file: " + ex.getMessage());
                    }
                }
            });
            buttonPanel.add(saveButton);

            JButton cancelButton = new JButton("Cancel");
            cancelButton.addActionListener(new ActionListener() {
                @Override
                public void actionPerformed(ActionEvent e) {
                    dialog.dispose();
                }
            });
            buttonPanel.add(cancelButton);

            dialog.add(buttonPanel, BorderLayout.SOUTH);

            dialog.pack();
            dialog.setLocationRelativeTo(this);
            dialog.setVisible(true);
        } catch (IOException ex) {
            JOptionPane.showMessageDialog(this, "Could not open file: " + ex.getMessage());
        }
    }
    
    private void createChildren(FileNode fileNode, DefaultMutableTreeNode node) {
        File[] files = fileNode.getFile().listFiles();
        if (files != null) {
            for (File file : files) {
                if (file.isDirectory()) {
                    FileNode childFileNode = new FileNode(file);
                    DefaultMutableTreeNode childNode = new DefaultMutableTreeNode(childFileNode);
                    node.add(childNode);
                    createChildren(childFileNode, childNode);
                }
            }
        }
    }

    private void showPopup(MouseEvent e, DefaultMutableTreeNode node) {
        JPopupMenu menu = new JPopupMenu();

        JMenuItem addKeyItem = new JMenuItem("Add Key");
        addKeyItem.addActionListener(event -> {
            String name = JOptionPane.showInputDialog(this, "Enter key name:");
            if (name != null && !name.isEmpty()) {
                try {
                    Files.createDirectories(Paths.get(((FileNode) node.getUserObject()).getFile().getAbsolutePath(), name));
                    refreshTree();
                } catch (IOException ex) {
                    JOptionPane.showMessageDialog(this, "Error creating directory: " + ex.getMessage());
                }
            }
        });
        menu.add(addKeyItem);

        JMenuItem addValueItem = new JMenuItem("Add Value");
        addValueItem.addActionListener(event -> {
            String name = JOptionPane.showInputDialog(this, "Enter value name:");
            if (name != null && !name.isEmpty()) {
                String value = JOptionPane.showInputDialog(this, "Enter value content:");
                try {
                    Files.write(Paths.get(((FileNode) node.getUserObject()).getFile().getAbsolutePath(), name), value.getBytes());
                    refreshTree();
                } catch (IOException ex) {
                    JOptionPane.showMessageDialog(this, "Error creating file: " + ex.getMessage());
                }
            }
        });
        menu.add(addValueItem);

        JMenuItem editKeyItem = new JMenuItem("Edit Key Name");
        editKeyItem.addActionListener(event -> {
            String name = JOptionPane.showInputDialog(this, "Enter new key name:");
            if (name != null && !name.isEmpty()) {
                File oldFile = ((FileNode) node.getUserObject()).getFile();
                File newFile = new File(oldFile.getParentFile(), name);
                if (!oldFile.renameTo(newFile)) {
                    JOptionPane.showMessageDialog(this, "Error renaming directory");
                }
                refreshTree();
            }
        });
        menu.add(editKeyItem);

        JMenuItem removeKeyItem = new JMenuItem("Remove Key");
        removeKeyItem.addActionListener(event -> {
            int result = JOptionPane.showConfirmDialog(this, "Deleting a key may cause serious issues. Do you want to proceed?", "Warning", JOptionPane.YES_NO_OPTION);
            if (result == JOptionPane.YES_OPTION) {
                try {
                    Files.walk(Paths.get(((FileNode) node.getUserObject()).getFile().getAbsolutePath()))
                        .map(Path::toFile)
                        .sorted((o1, o2) -> -o1.compareTo(o2))
                        .forEach(File::delete);
                    refreshTree();
                } catch(IOException ex) {
                    JOptionPane.showMessageDialog(this, "Error deleting directory: " + ex.getMessage());
                }
            }
        });
        menu.add(removeKeyItem);

        menu.show(e.getComponent(), e.getX(), e.getY());
    }
  
    private void refreshTree() {
        // Store expanded state
        ArrayList<File> expandedFiles = new ArrayList<>();
        for (int i = 0; i < directoryTree.getRowCount(); i++) {
            if (directoryTree.isExpanded(i)) {
                TreePath path = directoryTree.getPathForRow(i);
                DefaultMutableTreeNode node = (DefaultMutableTreeNode) path.getLastPathComponent();
                FileNode fileNode = (FileNode) node.getUserObject();
                expandedFiles.add(fileNode.getFile());
            }
        }

        // Refresh tree
        FileNode rootFileNode = new FileNode(new File(regPath));
        DefaultMutableTreeNode root = new DefaultMutableTreeNode(rootFileNode);
        treeModel.setRoot(root);
        createChildren(rootFileNode, root);

        // Restore expanded state
        for (File file : expandedFiles) {
            expandFile(directoryTree, file);
        }
        directoryTree.expandRow(0);
    }

    private void expandFile(JTree tree, File file) {
        FileNode rootNode = (FileNode) ((DefaultMutableTreeNode) tree.getModel().getRoot()).getUserObject();
        if (rootNode.getFile().equals(file)) {
            tree.expandPath(new TreePath(new Object[] { tree.getModel().getRoot() }));
            return;
        }

        expandFile(tree, file, (DefaultMutableTreeNode) tree.getModel().getRoot());
    }

    private boolean expandFile(JTree tree, File file, DefaultMutableTreeNode node) {
        FileNode fileNode = (FileNode) node.getUserObject();
        if (fileNode.getFile().equals(file)) {
            TreeNode[] pathNodes = node.getPath();
            TreePath path = new TreePath(pathNodes);
            tree.expandPath(path);
            return true;
        }

        for (int i = 0; i < node.getChildCount(); i++) {
            DefaultMutableTreeNode childNode = (DefaultMutableTreeNode) node.getChildAt(i);
            if (expandFile(tree, file, childNode)) {
                return true;
            }
        }

        return false;
    }

    public void expandAll(JTree tree, TreePath parent) {
        TreeNode node = (TreeNode) parent.getLastPathComponent();
        if (node.getChildCount() >= 0) {
            for (Enumeration e = node.children(); e.hasMoreElements(); ) {
                TreeNode n = (TreeNode) e.nextElement();
                TreePath path = parent.pathByAddingChild(n);
                expandAll(tree, path);
            }
        }
        tree.expandPath(parent);
    }


    public static void main(String[] args) {
        try {
            UIManager.setLookAndFeel(UIManager.getSystemLookAndFeelClassName());
        } catch (Exception ex) {
            ex.printStackTrace();
        }
        String path = args.length > 0 ? args[0] : "./registry";
        Regedit regedit = new Regedit(path);
        regedit.setDefaultCloseOperation(JFrame.EXIT_ON_CLOSE);
        regedit.setSize(800, 600);
        regedit.setVisible(true);
        regedit.refreshTree();
    }
}