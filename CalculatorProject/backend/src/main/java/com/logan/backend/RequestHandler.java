package com.logan.backend;

import java.util.List;

import org.springframework.beans.factory.annotation.Autowired;
import org.springframework.web.bind.annotation.CrossOrigin;
import org.springframework.web.bind.annotation.GetMapping;
import org.springframework.web.bind.annotation.PostMapping;
import org.springframework.web.bind.annotation.RequestBody;
import org.springframework.web.bind.annotation.RestController;

@RestController // this tells springboot that this class accepts HTTP requests
@CrossOrigin(origins = "http://localhost:5173") //allows the backend to accept web requests from the frontend so we are allowing requests from 5173
public class RequestHandler {

    // shorthard for declaring and initializing a new class instance instead of "= new"
    // an interface normally defines what methods exist, but the methods have no bodies so there is no code to run in an interface
    @Autowired
    private CalculationRepository calculationRepository;

    // handles an incoming POST request to this specific route. This is a public method that returns a "Calculation" object and the method name is saveCalculation.
    // the argument is the incoming @RequestBody converted into a "Calculation object" and then named calculation
    // calculationRepository is an instance of the CalculationRepository class which is an interface of Jpa repository which gives you methods like .save() to interact with a database
    @PostMapping("/api/history")
    public Calculation saveCalculation(@RequestBody Calculation calculation) {
        return calculationRepository.save(calculation);
    }

    // handles an incoming GET request to this URL
    @GetMapping("/api/history")
    public List<Calculation> getHistory() {
        return calculationRepository.findAll();
    }
}
