package com.jarvis.core.model;

import jakarta.persistence.*;

@Entity
@Table(name = "usuarios")
public class Usuario {
    
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;
    
    @Column(nullable = false)
    private String nombre;
    
    // Configuraciones de preferencias
    private String temaDashboard = "dark";

    public Usuario() {}

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }

    public String getNombre() { return nombre; }
    public void setNombre(String nombre) { this.nombre = nombre; }

    public String getTemaDashboard() { return temaDashboard; }
    public void setTemaDashboard(String temaDashboard) { this.temaDashboard = temaDashboard; }
}
