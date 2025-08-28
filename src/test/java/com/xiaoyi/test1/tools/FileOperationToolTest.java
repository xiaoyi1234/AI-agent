package com.xiaoyi.test1.tools;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class FileOperationToolTest {

    @Test
    public void readFile() {
        FileOperationTool tool = new FileOperationTool();
        String fileName = "test.txt";
        String result = tool.readFile(fileName);
        assertNotNull(result);
    }

    @Test
    public void writeFile() {
        FileOperationTool tool = new FileOperationTool();
        String fileName = "test.txt";
        String content = "这就是个测试文档";
        String result = tool.writeFile(fileName, content);
        assertNotNull(result);
    }
}