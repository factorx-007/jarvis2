package com.jarvis.core.websocket;

import com.fasterxml.jackson.databind.JsonNode;
import com.fasterxml.jackson.databind.ObjectMapper;
import com.fasterxml.jackson.databind.node.ObjectNode;
import com.jarvis.core.procesamiento_nlp.ProcesamientoLenguajeService;
import com.jarvis.core.memoria_personalizacion.LearningService;
import org.springframework.stereotype.Component;
import org.springframework.web.socket.CloseStatus;
import org.springframework.web.socket.TextMessage;
import org.springframework.web.socket.WebSocketSession;
import org.springframework.web.socket.handler.TextWebSocketHandler;

import java.util.Collections;
import java.util.Set;
import java.util.concurrent.ConcurrentHashMap;

@Component
public class JarvisWebSocketHandler extends TextWebSocketHandler {

    private final Set<WebSocketSession> sessions = Collections.newSetFromMap(new ConcurrentHashMap<>());
    private final ObjectMapper objectMapper = new ObjectMapper();
    private final ProcesamientoLenguajeService nlpService;
    private final LearningService learningService;

    public JarvisWebSocketHandler(ProcesamientoLenguajeService nlpService, LearningService learningService) {
        this.nlpService = nlpService;
        this.learningService = learningService;
    }

    @Override
    public void afterConnectionEstablished(WebSocketSession session) throws Exception {
        sessions.add(session);
        System.out.println("Nueva conexión WebSocket: " + session.getId());
    }

    @Override
    public void afterConnectionClosed(WebSocketSession session, CloseStatus status) throws Exception {
        sessions.remove(session);
        System.out.println("Conexión WebSocket cerrada: " + session.getId());
    }

    @Override
    protected void handleTextMessage(WebSocketSession session, TextMessage message) throws Exception {
        String payload = message.getPayload();
        System.out.println("Recibido: " + payload);

        JsonNode jsonNode = objectMapper.readTree(payload);
        
        if (jsonNode.has("source") && "voice".equals(jsonNode.get("source").asText())) {
            String rawText = jsonNode.get("raw_text").asText();
            
            // 1. NLP
            ProcesamientoLenguajeService.IntentResult nlpResult = nlpService.parseIntent(rawText);
            
            String target = nlpResult.target();
            String intent = nlpResult.intent();
            String ttsMessage = nlpResult.ttsMessage();

            // 2. Learning/Alias Resolution
            if ("LEARN_ALIAS".equals(intent)) {
                learningService.learnAlias(target);
            } else if (!"UNKNOWN_APP".equals(intent)) {
                target = learningService.resolveTarget(target);
            }

            // 3. Responder al Python Daemon
            ObjectNode responseNode = objectMapper.createObjectNode();
            responseNode.put("intent", intent);
            if (target != null) {
                responseNode.put("target", target);
            }
            if (ttsMessage != null) {
                responseNode.put("tts_message", ttsMessage);
            }
            
            broadcastMessage(objectMapper.writeValueAsString(responseNode));
            
            // 4. Guardar Historial
            learningService.recordInteraction(rawText, intent, target, ttsMessage);
            
            // 5. Broadcast to all UI clients (for dashboard update)
            ObjectNode eventNode = objectMapper.createObjectNode();
            eventNode.put("type", "HISTORY_UPDATE");
            ObjectNode dataNode = objectMapper.createObjectNode();
            dataNode.put("raw_text", rawText);
            dataNode.put("intent", intent);
            dataNode.put("target", target);
            eventNode.set("payload", dataNode);
            broadcastMessage(objectMapper.writeValueAsString(eventNode));
        } else if (jsonNode.has("source") && "llm".equals(jsonNode.get("source").asText())) {
            // El LLM en Python respondió. Lo enviamos directo al dashboard como un mensaje de "Juan".
            ObjectNode eventNode = objectMapper.createObjectNode();
            eventNode.put("type", "LLM_RESPONSE");
            eventNode.put("text", jsonNode.has("raw_text") ? jsonNode.get("raw_text").asText() : "");
            broadcastMessage(objectMapper.writeValueAsString(eventNode));
        }
    }
    
    private void broadcastMessage(String message) {
        for (WebSocketSession s : sessions) {
            try {
                if (s.isOpen()) {
                    s.sendMessage(new TextMessage(message));
                }
            } catch (Exception e) {
                e.printStackTrace();
            }
        }
    }
}
