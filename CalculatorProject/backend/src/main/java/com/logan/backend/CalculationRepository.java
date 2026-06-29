package com.logan.backend;

import org.springframework.data.jpa.repository.JpaRepository;

//interface mean CalucltionRepository HAS to impliment all of the partent class methods
public interface CalculationRepository extends JpaRepository<Calculation, Long> {
}