package com.xiaoyi.test1.tools;
import cn.hutool.http.HttpUtil;
import cn.hutool.json.JSONArray;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;
import org.springframework.ai.tool.annotation.Tool;
import org.springframework.ai.tool.annotation.ToolParam;
import org.springframework.stereotype.Component;

import java.util.ArrayList;
import java.util.HashMap;
import java.util.List;
import java.util.Map;
import java.util.stream.Collectors;


@Component
public class SearXNGSearchTool {

    @Tool(description = "Search for information from SearXNG Engine")
    public String searchWeb(@ToolParam(description = "Search query keyword") String query){
        Map<String, Object> paramMap = new HashMap<>();
        paramMap.put("q", query);
        paramMap.put("format", "json");
        paramMap.put("num_results", "5"); // 限制返回5条结果
        try{
            String response = HttpUtil.get("http://localhost:6080/search", paramMap);
            // 解析JSON为List<Map>（假设返回格式为{"results": [...]})
            //List<Map> results = JSONUtil.parseArray(response).toList(Map.class);

            JSONObject jsonObject = JSONUtil.parseObj(response);
            JSONArray organicResults = jsonObject.getJSONArray("results");
            List<Map<String, Object>> results = new ArrayList<>();
            for (int i = 0; i < organicResults.size(); i++) {
                JSONObject item = organicResults.getJSONObject(i);
                Map<String, Object> map = item.toBean(Map.class);
                results.add(map);
            }
            // 截取前5条并格式化输出
            return results.stream()
                    .limit(5)
                    .map(result -> String.format("- 标题：%s\n  内容：%s\n  链接：%s",
                            result.get("title"),
                            result.get("content"),
                            result.get("url")))
                    .collect(Collectors.joining(System.lineSeparator()));
        }catch (Exception e){
            return  "Error searching searXNG:" + e.getMessage();
        }

    }


}
