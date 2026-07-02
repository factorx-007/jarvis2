package com.jarvis.core.model;

import jakarta.persistence.*;

@Entity
@Table(name = "comando_alias")
public class ComandoAlias {

    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false, unique = true)
    private String alias;
    
    @Column(nullable = false)
    private String targetApp;
    
    // Indica si el sistema lo aprendió automáticamente
    private boolean aprendido = false;

    public ComandoAlias() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getAlias() { return alias; }
    public void setAlias(String alias) { this.alias = alias; }

    public String getTargetApp() { return targetApp; }
    public void setTargetApp(String targetApp) { this.targetApp = targetApp; }

    public boolean isAprendido() { return aprendido; }
    public void setAprendido(boolean aprendido) { this.aprendido = aprendido; }
}
