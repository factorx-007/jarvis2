package com.jarvis.core.nlp;

import org.springframework.stereotype.Service;

@Service
public class NLPService {

    public IntentResult parseIntent(String text) {
        if (text == null || text.isBlank()) {
            return new IntentResult("UNKNOWN", null);
        }
        
        String normalized = text.toLowerCase().trim();
        
        // Reglas muy básicas para abrir/cerrar
        if (normalized.startsWith("abre ") || normalized.startsWith("abrir ")) {
            String target = normalized.replaceFirst("abre |abrir ", "").trim();
            target = cleanArticles(target);
            return new IntentResult("OPEN_APP", target);
        } else if (normalized.startsWith("cierra ") || normalized.startsWith("cerrar ")) {
            String target = normalized.replaceFirst("cierra |cerrar ", "").trim();
            target = cleanArticles(target);
            return new IntentResult("CLOSE_APP", target);
        } else if (normalized.startsWith("aprende ") || normalized.startsWith("aprender ")) {
            return new IntentResult("LEARN_ALIAS", normalized.replaceFirst("aprende |aprender ", "").trim());
        }
        
        return new IntentResult("UNKNOWN", null);
    }
    
    private String cleanArticles(String target) {
        if (target == null) return null;
        if (target.startsWith("la ")) return target.substring(3).trim();
        if (target.startsWith("el ")) return target.substring(3).trim();
        if (target.startsWith("los ")) return target.substring(4).trim();
        if (target.startsWith("las ")) return target.substring(4).trim();
        if (target.startsWith("un ")) return target.substring(3).trim();
        if (target.startsWith("una ")) return target.substring(4).trim();
        return target;
    }

    public record IntentResult(String intent, String target) {}
}
