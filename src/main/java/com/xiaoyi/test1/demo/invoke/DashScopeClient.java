package com.xiaoyi.test1.demo.invoke;

import cn.hutool.http.HttpRequest;
import cn.hutool.json.JSONObject;
import cn.hutool.json.JSONUtil;

public class DashScopeClient {
    private static final String API_URL = "https://dashscope.aliyuncs.com/api/v1/services/aigc/text-generation/generation";
    private final String apiKey;

    public DashScopeClient(String apiKey) {
        this.apiKey = apiKey;
    }

    public String generateText(String userContent) {
        // 构建请求体
        JSONObject requestBody = new JSONObject();
        requestBody.set("model", "qwen-plus");
        
        // 构建messages数组
        JSONObject systemMessage = new JSONObject();
        systemMessage.set("role", "system");
        systemMessage.set("content", "You are a helpful assistant.");

        JSONObject userMessage = new JSONObject();
        userMessage.set("role", "user");
        userMessage.set("content", userContent);

        // 构建input对象
        JSONObject input = new JSONObject();
        input.set("messages", JSONUtil.createArray().set(systemMessage).set(userMessage));
        requestBody.set("input", input);

        // 构建parameters对象
        JSONObject parameters = new JSONObject();
        parameters.set("result_format", "message");
        requestBody.set("parameters", parameters);

        // 发送HTTP请求
        String result = HttpRequest.post(API_URL)
                .header("Authorization", "Bearer " + apiKey)
                .header("Content-Type", "application/json")
                .body(requestBody.toString())
                .execute()
                .body();

        return result;
    }
}

