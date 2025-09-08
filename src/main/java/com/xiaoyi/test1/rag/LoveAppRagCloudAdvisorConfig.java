package com.xiaoyi.test1.rag;

import com.alibaba.cloud.ai.dashscope.api.DashScopeAgentApi;


import com.alibaba.cloud.ai.dashscope.api.DashScopeApi;
import com.alibaba.cloud.ai.dashscope.rag.DashScopeDocumentRetriever;
import com.alibaba.cloud.ai.dashscope.rag.DashScopeDocumentRetrieverOptions;
import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.chat.client.advisor.api.Advisor;
import org.springframework.ai.rag.advisor.RetrievalAugmentationAdvisor;
import org.springframework.ai.rag.retrieval.search.DocumentRetriever;
import org.springframework.beans.factory.annotation.Value;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;

//@Configuration
@Slf4j
public class LoveAppRagCloudAdvisorConfig {
    @Value("sk-40c20d941b524614bc5b19d8c6803a63")
    private String dashScopeapikey;

    @Bean
    public Advisor loveAppRagCloudAdvisor(){
        //调用大模型api
        var dashScopeApi = DashScopeApi.builder()
                .apiKey(dashScopeapikey)
                .build();

        // 创建文档检索器
        DocumentRetriever retriever = new DashScopeDocumentRetriever(dashScopeApi,
                DashScopeDocumentRetrieverOptions.builder()
                        .withIndexName("pcie1")
                        .build());
        return RetrievalAugmentationAdvisor.builder()
                .documentRetriever(retriever)
                .build();
    }


}
