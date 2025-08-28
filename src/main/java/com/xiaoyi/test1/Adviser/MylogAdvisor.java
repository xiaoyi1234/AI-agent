package com.xiaoyi.test1.Adviser;

import java.util.function.Function;

import org.slf4j.Logger;
import org.slf4j.LoggerFactory;
import reactor.core.publisher.Flux;

import org.springframework.ai.chat.client.advisor.api.AdvisedRequest;
import org.springframework.ai.chat.client.advisor.api.AdvisedResponse;
import org.springframework.ai.chat.client.advisor.api.CallAroundAdvisor;
import org.springframework.ai.chat.client.advisor.api.CallAroundAdvisorChain;
import org.springframework.ai.chat.client.advisor.api.StreamAroundAdvisor;
import org.springframework.ai.chat.client.advisor.api.StreamAroundAdvisorChain;
import org.springframework.ai.chat.model.ChatResponse;
import org.springframework.ai.chat.model.MessageAggregator;
import org.springframework.ai.model.ModelOptionsUtils;

/**
 * A simple logger advisor that logs the request and response messages.
 *
 * @author Christian Tzolov
 */
public class MylogAdvisor implements CallAroundAdvisor, StreamAroundAdvisor {

    public static final Function<AdvisedRequest, String> DEFAULT_REQUEST_TO_STRING = request -> request.toString();

    public static final Function<ChatResponse, String> DEFAULT_RESPONSE_TO_STRING = response -> ModelOptionsUtils
            .toJsonStringPrettyPrinter(response);

    private static final Logger logger = LoggerFactory.getLogger(MylogAdvisor.class);

    private final Function<AdvisedRequest, String> requestToString;

    private final Function<ChatResponse, String> responseToString;


    public MylogAdvisor() {
        this(DEFAULT_REQUEST_TO_STRING, DEFAULT_RESPONSE_TO_STRING, 100);
    }


    public MylogAdvisor(Function<AdvisedRequest, String> requestToString,
                        Function<ChatResponse, String> responseToString, int order) {
        this.requestToString = requestToString;
        this.responseToString = responseToString;
    }

    @Override
    public String getName() {
        return "xiaoyi123";
    }

    @Override
    public int getOrder() {
        return 100;
    }

    private AdvisedRequest before(AdvisedRequest request) {
        logger.debug("request: {}", this.requestToString.apply(request));
        return request;
    }

    private void observeAfter(AdvisedResponse advisedResponse) {
        logger.debug("response: {}", this.responseToString.apply(advisedResponse.response()));
    }

    public String toString() {
        return MylogAdvisor.class.getSimpleName();
    }

    @Override
    public AdvisedResponse aroundCall(AdvisedRequest advisedRequest, CallAroundAdvisorChain chain) {

        advisedRequest = before(advisedRequest);

        AdvisedResponse advisedResponse = chain.nextAroundCall(advisedRequest);

        observeAfter(advisedResponse);

        return advisedResponse;
    }

    @Override
    public Flux<AdvisedResponse> aroundStream(AdvisedRequest advisedRequest, StreamAroundAdvisorChain chain) {

        advisedRequest = before(advisedRequest);

        Flux<AdvisedResponse> advisedResponses = chain.nextAroundStream(advisedRequest);

        return new MessageAggregator().aggregateAdvisedResponse(advisedResponses, this::observeAfter);
    }

}
