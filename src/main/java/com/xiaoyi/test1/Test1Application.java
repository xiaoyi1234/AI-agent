package com.xiaoyi.test1;

import org.jetbrains.annotations.TestOnly;
import org.springframework.ai.autoconfigure.vectorstore.pgvector.PgVectorStoreAutoConfiguration;
import org.springframework.boot.SpringApplication;
import org.springframework.boot.SpringBootConfiguration;
import org.springframework.boot.autoconfigure.SpringBootApplication;
import org.springframework.boot.autoconfigure.jdbc.DataSourceAutoConfiguration;

@SpringBootApplication(exclude = {
        PgVectorStoreAutoConfiguration.class
        // 为了便于大家开发调试和部署，取消数据库自动配置，需要使用 PgVector 时把 DataSourceAutoConfiguration.class 删除
        , DataSourceAutoConfiguration.class
})

public class Test1Application {

    public static void main(String[] args) {

        SpringApplication.run(Test1Application.class, args);
    }

}
