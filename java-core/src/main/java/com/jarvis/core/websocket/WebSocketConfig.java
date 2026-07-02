package com.jarvis.core.websocket;

import org.springframework.context.annotation.Configuration;
import org.springframework.web.socket.config.annotation.EnableWebSocket;
import org.springframework.web.socket.config.annotation.WebSocketConfigurer;
import org.springframework.web.socket.config.annotation.WebSocketHandlerRegistry;

@Configuration
@EnableWebSocket
public class WebSocketConfig implements WebSocketConfigurer {

    private final JarvisWebSocketHandler jarvisWebSocketHandler;

    public WebSocketConfig(JarvisWebSocketHandler jarvisWebSocketHandler) {
        this.jarvisWebSocketHandler = jarvisWebSocketHandler;
    }

    @Override
    public void registerWebSocketHandlers(WebSocketHandlerRegistry registry) {
        registry.addHandler(jarvisWebSocketHandler, "/jarvis-ws").setAllowedOrigins("*");
    }
}
