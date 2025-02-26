package com.example.board.security;

import org.springframework.context.annotation.Bean;
import org.springframework.context.annotation.Configuration;
import org.springframework.security.config.annotation.authentication.builders.AuthenticationManagerBuilder;
import org.springframework.security.config.annotation.web.builders.HttpSecurity;
import org.springframework.security.config.annotation.web.configuration.EnableWebSecurity;
import org.springframework.security.config.annotation.web.configuration.WebSecurityConfigurerAdapter;
import org.springframework.security.crypto.bcrypt.BCryptPasswordEncoder;
import org.springframework.security.crypto.password.PasswordEncoder;

@Configuration
@EnableWebSecurity
public class WebSecurityConfig extends WebSecurityConfigurerAdapter {

    @Override
    protected void configure(HttpSecurity http) throws Exception {
         http.authorizeRequests()
             .antMatchers("/login", "/css/**").permitAll()
             .anyRequest().authenticated()
             .and()
             .formLogin()
             .loginPage("/login")
             .defaultSuccessUrl("/board/list")
             .and()
             .logout()
             .logoutSuccessUrl("/login")
             .and()
             .csrf().disable(); // 테스트 목적일 경우 CSRF 비활성화 (실제 서비스 시에는 활성화 권장)
    }

    @Override
    protected void configure(AuthenticationManagerBuilder auth) throws Exception {
         // In-Memory 방식의 간단한 사용자 인증 (실제 서비스에서는 DB 기반 사용자 관리 권장)
         auth.inMemoryAuthentication()
             .withUser("user").password(passwordEncoder().encode("password")).roles("USER");
    }

    @Bean
    public PasswordEncoder passwordEncoder() {
         return new BCryptPasswordEncoder();
    }
}
