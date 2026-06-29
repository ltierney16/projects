package com.logan.backend;

import java.time.LocalDateTime;

import jakarta.persistence.Entity; // apart of JPA
import jakarta.persistence.GeneratedValue;
import jakarta.persistence.GenerationType;
import jakarta.persistence.Id;

// entity tells springboot that this class represents a database row
@Entity
public class Calculation {

    //this marks which field in the database is the ID for the row
    @Id
    @GeneratedValue(strategy = GenerationType.IDENTITY)
    private Long id;

    private String expression;
    private String result;
    private LocalDateTime timestamp;

    public Calculation() {}

    public Calculation(String expression, String result) {
        this.expression = expression;
        this.result = result;
        this.timestamp = LocalDateTime.now();
    }

    public Long getId() { return id; }
    public void setId(Long id) { this.id = id; }
    public String getExpression() { return expression; }
    public void setExpression(String expression) { this.expression = expression; }
    public String getResult() { return result; }
    public void setResult(String result) { this.result = result; }
    public LocalDateTime getTimestamp() { return timestamp; }
    public void setTimestamp(LocalDateTime timestamp) { this.timestamp = timestamp; }
}