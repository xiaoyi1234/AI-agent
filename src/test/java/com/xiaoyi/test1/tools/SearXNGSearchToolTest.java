package com.xiaoyi.test1.tools;

import org.junit.jupiter.api.Test;

import static org.junit.jupiter.api.Assertions.*;

class SearXNGSearchToolTest {

    @Test
    void searchWeb() {
        SearXNGSearchTool searchTool = new SearXNGSearchTool();
        String query = "上海美食推荐";
        String result = searchTool.searchWeb(query);
        assertNotNull(result);
    }
}