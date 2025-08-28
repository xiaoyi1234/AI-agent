package com.xiaoyi.test1.demo.invoke;

public class HttpInvoke {
    public static void main(String[] args) {
        String apiKey = TestApikey.apikey;
        DashScopeClient client = new DashScopeClient(apiKey);
        String response = client.generateText("机器死机了吗？");
        System.out.println(response);
    }
}
