package com.xiaoyi.test1.App;

import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversation;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationParam;
import com.alibaba.dashscope.aigc.multimodalconversation.MultiModalConversationResult;
import com.alibaba.dashscope.common.MultiModalMessage;
import com.alibaba.dashscope.common.Role;
import com.alibaba.dashscope.exception.NoApiKeyException;
import com.alibaba.dashscope.exception.UploadFileException;
import com.alibaba.nacos.api.NacosFactory;
import com.alibaba.nacos.api.PropertyKeyConst;
import com.alibaba.nacos.api.ai.AiFactory;
import com.alibaba.nacos.api.ai.AiService;
import com.alibaba.nacos.api.ai.model.mcp.McpServerDetailInfo;
import com.alibaba.nacos.api.config.ConfigService;
import com.alibaba.nacos.api.config.listener.Listener;
import com.alibaba.nacos.api.exception.NacosException;

import com.alibaba.nacos.common.utils.JacksonUtils;
import com.xiaoyi.test1.Adviser.MylogAdvisor;
import jakarta.annotation.Resource;

import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.client.advisor.vectorstore.QuestionAnswerAdvisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.InMemoryChatMemoryRepository;
import org.springframework.ai.chat.memory.MessageWindowChatMemory;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.image.*;

import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.beans.factory.annotation.Qualifier;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;

import java.util.*;
import java.util.concurrent.Executor;


@Component
@Slf4j
public class LoveApp {

    private final ChatClient chatClient;
    private final ImageModel imageModel;


    private static final String SYSTEM_PROMPT = "扮演资深程序员";

    public LoveApp(ChatModel dashscopeChatModel,  ImageModel dashScopeImageModel) {
        this.imageModel = dashScopeImageModel;

        // 初始化基于内存的对话记忆
//        String FileDir = System.getProperty("user.dir")+"/chat-memory";
//        ChatMemory chatMemory = new FileBasedChatMemory(FileDir);
        MessageWindowChatMemory chatMemory = MessageWindowChatMemory.builder()
                .chatMemoryRepository(new InMemoryChatMemoryRepository())
                .maxMessages(10)
                .build();
        chatClient = ChatClient.builder(dashscopeChatModel)
                .defaultSystem(SYSTEM_PROMPT)
                .defaultAdvisors(
                        new MylogAdvisor(),
                        MessageChatMemoryAdvisor.builder(chatMemory).build()
                        //new ReReadingAdvisor()
                )
                .build();

    }

    public String doChat(String message, String chatId) {
        ChatResponse response = chatClient
                .prompt()
                .user(message)
                .advisors(spec -> spec.param(ChatMemory.CONVERSATION_ID, chatId))
                .call()
                .chatResponse();
        String content = null;
        if (response != null) {
            content = response.getResult().getOutput().getText();
        }
        log.info("content: {}", content);
        return content;
    }

    @Resource
    private ToolCallback[] allTools;
    public Flux<String> doChatByStream(String message, String chatId){
        return  chatClient.prompt()
                .user(message)
                .advisors(spec -> spec.param(ChatMemory.CONVERSATION_ID, chatId))
                .toolCallbacks(allTools)
                .stream()
                .content();

    }


    public record LoveReport(String title, List<String> suggestions) { }
    public LoveReport doChatWithReport(String message, String chatId) {
        LoveReport response = chatClient
                .prompt()
                .system(SYSTEM_PROMPT+"每次对话后都要生成咨询结果，标题为{用户名}的报告，内容为建议的列表")
                .user(message)
                .advisors(spec -> spec.param(ChatMemory.CONVERSATION_ID, chatId))
                .call()
                .entity(LoveReport.class);

        log.info("content: {}", response);
        return response;
    }

    @Resource
    private VectorStore loveAppVectorStore;
//    @Resource
//    private QueryRewriter queryRewriter;
//    @Resource
//    private  VectorStore pgVectorVectorStore;
//    @Resource
//    private Advisor loveAppRagCloudAdvisor;

    /**
     * @param message
     * @param chatId
     * @return
     */
    public String doChatWithRag(String message, String chatId) {
//        String rewritedMessage = queryRewriter.doQueryRewrite(message);
        ChatResponse response = chatClient
                .prompt()
                .user(message)
                .advisors(spec -> spec.param(ChatMemory.CONVERSATION_ID, chatId))
                // 开启日志，便于观察效果
                .advisors(new MylogAdvisor())
                // 应用自定义的 RAG 检索增强服务（文档查询器 + 上下文增强器）??
                //.advisors(LoveAppRagCustomAdvisorFactory.createLoveAppRagCustomAdvisor(loveAppVectorStore,"pcie-gen5.md"))
                // 应用 RAG 知识库问答
                .advisors(QuestionAnswerAdvisor.builder(loveAppVectorStore).build())
                // 应用 RAG 检索增强服务（基于 PgVector 向量存储）
//                .advisors(new QuestionAnswerAdvisor(pgVectorVectorStore))
                // 应用增强检索服务（云知识库服务）
//                .advisors(loveAppRagCloudAdvisor)

                .call()
                .chatResponse();
            String content = response.getResult().getOutput().getText();

        log.info("content: {}", content);
        return content;
    }


    public String doChatWithTools(String message, String chatId) {
        ChatResponse response = chatClient
                .prompt()
                .user(message)
                .advisors(spec -> spec.param(ChatMemory.CONVERSATION_ID, chatId))
                // 开启日志，便于观察效果
                .advisors(new MylogAdvisor())
                .toolCallbacks(allTools)
                .call()
                .chatResponse();
        String content = response.getResult().getOutput().getText();
        log.info("content: {}", content);
        return content;
    }

    @Autowired
    @Qualifier("loadbalancedMcpSyncToolCallbacks")
    ToolCallbackProvider toolCallbackProvider;

    public String doChatWithMcp(String message, String chatId) {
        ChatResponse response = chatClient
                .prompt()
                .user(message)
                .advisors(spec -> spec.param(ChatMemory.CONVERSATION_ID, chatId))
                // 开启日志，便于观察效果
                .advisors(new MylogAdvisor())
                .toolCallbacks(toolCallbackProvider)
                .call()
                .chatResponse();
        String content = response.getResult().getOutput().getText();
        log.info("content: {}", content);
        return content;
    }

    public final String apiKey = System.getenv("DASHSCOPE_API_KEY");
    public String  doImage(String message) throws InterruptedException, NoApiKeyException, UploadFileException {

        MultiModalConversation conv = new MultiModalConversation();

        MultiModalMessage userMessage = MultiModalMessage.builder().role(Role.USER.getValue())
                .content(Arrays.asList(
                        Collections.singletonMap("text", message)
                )).build();
        Map<String, Object> parameters = new HashMap<>();
        parameters.put("watermark", true);
        parameters.put("prompt_extend", true);
        parameters.put("negative_prompt", "");
        parameters.put("size", "1328*1328");

        MultiModalConversationParam param = MultiModalConversationParam.builder()
                .apiKey(apiKey)
                .model("qwen-image")
                .messages(Collections.singletonList(userMessage))
                .parameters(parameters)
                .build();

        MultiModalConversationResult result = conv.call(param);

        return result.getOutput().getChoices().get(0).getMessage().getContent().get(0).get("image").toString();

    }

    public Boolean setNacosConfig(String dataId, String group, String content){
        try {
            // 初始化配置服务，控制台通过示例代码自动获取下面参数
            String serverAddr = "127.0.0.1:8848";
            Properties properties = new Properties();
            properties.put("serverAddr", serverAddr);
            ConfigService configService = NacosFactory.createConfigService(properties);
            boolean isPublishOk = configService.publishConfig(dataId, group, content);
            return isPublishOk;
        } catch (NacosException e) {
            log.error(e.getMessage());
            return false;
        }
    }

    public String getNacosConfig(String dataId, String group) {
        try {
            String serverAddr = "127.0.0.1:8848";
            Properties properties = new Properties();
            properties.put("serverAddr", serverAddr);
//            ConfigService configService = NacosFactory.createConfigService(properties);
//            Listener listener = new Listener() {
//                @Override
//                public Executor getExecutor() {
//                    return null;
//                }
//
//                @Override
//                public void receiveConfigInfo(String configInfo) {
//                    log.info("configInfo: {}", configInfo);
//                }
//            };
//            String content = configService.getConfigAndSignListener(dataId, group, 5000, listener);
//            configService.removeListener(dataId, group, listener);

            AiService aiService = AiFactory.createAiService(properties);
            McpServerDetailInfo detailInfo = aiService.getMcpServer("mcp-image-search", null);
            System.out.println(JacksonUtils.toJson(detailInfo));
            return detailInfo.toString();
//            return content;
        } catch (NacosException e) {
            log.error(e.getMessage());
            return "get nacos config error";
        }

    }
}

