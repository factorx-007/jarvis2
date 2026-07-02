package com.jarvis.core.model;

import jakarta.persistence.*;
import java.time.LocalDateTime;

@Entity
@Table(name = "historial_interaccion")
public class HistorialInteraccion {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    private LocalDateTime timestamp;
    
    @Column(nullable = false)
    private String inputCrudo;
    
    private String intentResuelto;
    private String targetResuelto;
    private String respuestaGenerada;

    public HistorialInteraccion() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }

    public String getInputCrudo() { return inputCrudo; }
    public void setInputCrudo(String inputCrudo) { this.inputCrudo = inputCrudo; }

    public String getIntentResuelto() { return intentResuelto; }
    public void setIntentResuelto(String intentResuelto) { this.intentResuelto = intentResuelto; }

    public String getTargetResuelto() { return targetResuelto; }
    public void setTargetResuelto(String targetResuelto) { this.targetResuelto = targetResuelto; }

    public String getRespuestaGenerada() { return respuestaGenerada; }
    public void setRespuestaGenerada(String respuestaGenerada) { this.respuestaGenerada = respuestaGenerada; }
}
