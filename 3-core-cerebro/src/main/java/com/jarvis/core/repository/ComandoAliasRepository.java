package com.jarvis.core.repository;

import com.jarvis.core.model.ComandoAlias;
import org.springframework.data.jpa.repository.JpaRepository;
import java.util.Optional;

public interface ComandoAliasRepository extends JpaRepository<ComandoAlias, Long> {
    Optional<ComandoAlias> findByAlias(String alias);
}
