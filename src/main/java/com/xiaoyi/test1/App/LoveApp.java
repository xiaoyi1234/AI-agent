package com.xiaoyi.test1.App;

import com.xiaoyi.test1.Adviser.MylogAdvisor;
import com.xiaoyi.test1.rag.LoveAppRagCloudAdvisorConfig;
import com.xiaoyi.test1.rag.LoveAppRagCustomAdvisorFactory;
import com.xiaoyi.test1.rag.QueryRewriter;
import jakarta.annotation.Resource;

import lombok.extern.slf4j.Slf4j;
import org.springframework.ai.chat.client.ChatClient;
import org.springframework.ai.chat.client.advisor.MessageChatMemoryAdvisor;
import org.springframework.ai.chat.client.advisor.QuestionAnswerAdvisor;
import org.springframework.ai.chat.client.advisor.api.Advisor;
import org.springframework.ai.chat.memory.ChatMemory;
import org.springframework.ai.chat.memory.InMemoryChatMemory;
import org.springframework.ai.chat.model.ChatModel;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.tool.ToolCallback;
import org.springframework.ai.tool.ToolCallbackProvider;
import org.springframework.ai.vectorstore.VectorStore;
import org.springframework.stereotype.Component;
import reactor.core.publisher.Flux;

import java.util.List;

import static org.springframework.ai.chat.client.advisor.AbstractChatMemoryAdvisor.CHAT_MEMORY_CONVERSATION_ID_KEY;
import static org.springframework.ai.chat.client.advisor.AbstractChatMemoryAdvisor.CHAT_MEMORY_RETRIEVE_SIZE_KEY;


@Component
@Slf4j
public class LoveApp {

    private final ChatClient chatClient;


    private static final String SYSTEM_PROMPT = "扮演资深程序员";

    public LoveApp(ChatModel dashscopeChatModel) {
        // 初始化基于内存的对话记忆

//        String FileDir = System.getProperty("user.dir")+"/chat-memory";
//        ChatMemory chatMemory = new FileBasedChatMemory(FileDir);
        ChatMemory chatMemory = new InMemoryChatMemory();
        chatClient = ChatClient.builder(dashscopeChatModel)
                .defaultSystem(SYSTEM_PROMPT)
                .defaultAdvisors(
                        new MessageChatMemoryAdvisor(chatMemory),
                        new MylogAdvisor()
                        //new ReReadingAdvisor()
                )
                .build();
    }

    public String doChat(String message, String chatId) {
        ChatResponse response = chatClient
                .prompt()
                .user(message)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 3))
                .call()
                .chatResponse();
        String content = null;
        if (response != null) {
            content = response.getResult().getOutput().getText();
        }
        log.info("content: {}", content);
        return content;
    }

    public Flux<String> doChatByStream(String message, String chatId){
        return  chatClient.prompt()
                .user(message)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 3))
                .stream()
                .content();

    }


    public record LoveReport(String title, List<String> suggestions) { }
    public LoveReport doChatWithReport(String message, String chatId) {
        LoveReport response = chatClient
                .prompt()
                .system(SYSTEM_PROMPT+"每次对话后都要生成咨询结果，标题为{用户名}的报告，内容为建议的列表")
                .user(message)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 3))
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
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 3))
                // 开启日志，便于观察效果
                .advisors(new MylogAdvisor())
                // 应用自定义的 RAG 检索增强服务（文档查询器 + 上下文增强器）??
                //.advisors(LoveAppRagCustomAdvisorFactory.createLoveAppRagCustomAdvisor(loveAppVectorStore,"pcie-gen5.md"))
                // 应用 RAG 知识库问答
                .advisors(new QuestionAnswerAdvisor(loveAppVectorStore))
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

    @Resource
    private ToolCallback[] allTools;

    public String doChatWithTools(String message, String chatId) {
        ChatResponse response = chatClient
                .prompt()
                .user(message)
                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 10))
                // 开启日志，便于观察效果
                .advisors(new MylogAdvisor())
                .tools(allTools)
                .call()
                .chatResponse();
        String content = response.getResult().getOutput().getText();
        log.info("content: {}", content);
        return content;
    }

//    @Resource
//    private ToolCallbackProvider toolCallbackProvider;
//
//    public String doChatWithMcp(String message, String chatId) {
//        ChatResponse response = chatClient
//                .prompt()
//                .user(message)
//                .advisors(spec -> spec.param(CHAT_MEMORY_CONVERSATION_ID_KEY, chatId)
//                        .param(CHAT_MEMORY_RETRIEVE_SIZE_KEY, 10))
//                // 开启日志，便于观察效果
//                .advisors(new MylogAdvisor())
//                .tools(toolCallbackProvider)
//                .call()
//                .chatResponse();
//        String content = response.getResult().getOutput().getText();
//        log.info("content: {}", content);
//        return content;
//    }

}

