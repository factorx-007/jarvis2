package com.jarvis.core.service;

import com.jarvis.core.model.ComandoAlias;
import com.jarvis.core.model.HistorialInteraccion;
import com.jarvis.core.repository.ComandoAliasRepository;
import com.jarvis.core.repository.HistorialInteraccionRepository;
import org.springframework.stereotype.Service;

import java.time.LocalDateTime;
import java.util.Optional;

@Service
public class LearningService {

    private final ComandoAliasRepository aliasRepository;
    private final HistorialInteraccionRepository historialRepository;

    public LearningService(ComandoAliasRepository aliasRepository, HistorialInteraccionRepository historialRepository) {
        this.aliasRepository = aliasRepository;
        this.historialRepository = historialRepository;
    }

    public String resolveTarget(String target) {
        if (target == null) return null;
        Optional<ComandoAlias> aliasOpt = aliasRepository.findByAlias(target);
        return aliasOpt.map(ComandoAlias::getTargetApp).orElse(target);
    }
    
    public void learnAlias(String textToLearn) {
        // Formato esperado: "aprende [alias] como [target]"
        if (textToLearn.contains(" como ")) {
            String[] parts = textToLearn.split(" como ");
            if (parts.length == 2) {
                String alias = parts[0].trim();
                String target = parts[1].trim();
                
                ComandoAlias newAlias = new ComandoAlias();
                newAlias.setAlias(alias);
                newAlias.setTargetApp(target);
                newAlias.setAprendido(true);
                
                aliasRepository.save(newAlias);
            }
        }
    }

    public HistorialInteraccion recordInteraction(String rawText, String intent, String target, String response) {
        HistorialInteraccion historial = new HistorialInteraccion();
        historial.setTimestamp(LocalDateTime.now());
        historial.setInputCrudo(rawText);
        historial.setIntentResuelto(intent);
        historial.setTargetResuelto(target);
        historial.setRespuestaGenerada(response);
        return historialRepository.save(historial);
    }
}
