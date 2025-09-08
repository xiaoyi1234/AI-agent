package com.xiaoyi.test1.Adviser;

import java.util.function.Function;

import lombok.extern.slf4j.Slf4j;
import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import org.springframework.ai.chat.client.ChatClientMessageAggregator;
import org.springframework.ai.chat.client.ChatClientRequest;
import org.springframework.ai.chat.client.ChatClientResponse;

import org.springframework.ai.chat.client.advisor.api.*;
import org.springframework.ai.chat.model.ChatResponse;
import reactor.core.publisher.Flux;
import org.springframework.ai.model.ModelOptionsUtils;

/**
 * A simple logger advisor that logs the request and response messages.
 *
 * @author Christian Tzolov
 */
@Slf4j
public class MylogAdvisor implements CallAdvisor, StreamAdvisor {

    public static final Function<ChatClientRequest, String> DEFAULT_REQUEST_TO_STRING = ChatClientRequest::toString;
    public static final Function<ChatResponse, String> DEFAULT_RESPONSE_TO_STRING = ModelOptionsUtils::toJsonStringPrettyPrinter;

    private static final Logger logger = LoggerFactory.getLogger(MylogAdvisor.class);

    private final Function<ChatClientRequest, String> requestToString;

    private final Function<ChatResponse, String> responseToString;
    private final int order;


    public MylogAdvisor() {
        this(DEFAULT_REQUEST_TO_STRING, DEFAULT_RESPONSE_TO_STRING, 100);
    }


    public MylogAdvisor(Function<ChatClientRequest, String> requestToString,
                        Function<ChatResponse, String> responseToString, int order) {
        this.requestToString = requestToString;
        this.responseToString = responseToString;
        this.order = order;
    }

    @Override
    public String getName() {
        return this.getClass().getSimpleName();
    }

    @Override
    public int getOrder() {
        return 0;
    }

    private ChatClientRequest before(ChatClientRequest request) {
        logger.debug("request: {}", request.prompt());
        return request;
    }

    private void observeAfter(ChatClientResponse chatClientResponse) {
        logger.debug("response: {}", chatClientResponse.chatResponse().getResult().getOutput().getText());
    }

    public String toString() {
        return MylogAdvisor.class.getSimpleName();
    }

    @Override
    public ChatClientResponse adviseCall(ChatClientRequest chatClientRequest, CallAdvisorChain chain) {

        chatClientRequest = before(chatClientRequest);

        ChatClientResponse chatClientResponse = chain.nextCall(chatClientRequest);

        observeAfter(chatClientResponse);

        return chatClientResponse;
    }

    @Override
    public Flux<ChatClientResponse> adviseStream(ChatClientRequest chatClientRequest, StreamAdvisorChain chain) {

        chatClientRequest = before(chatClientRequest);

        Flux<ChatClientResponse> chatClientResponses = chain.nextStream(chatClientRequest);

        return (new ChatClientMessageAggregator()).aggregateChatClientResponse(chatClientResponses, this::observeAfter);
    }

}
