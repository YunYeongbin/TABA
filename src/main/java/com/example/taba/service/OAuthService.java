package com.example.taba.service;

import com.example.taba.model.GithubUser;
import com.example.taba.model.OAuthInfo;
import com.google.gson.JsonElement;
import com.google.gson.JsonObject;
import com.google.gson.JsonParser;
import lombok.extern.slf4j.Slf4j;
import org.springframework.http.*;
import org.springframework.http.converter.FormHttpMessageConverter;
import org.springframework.http.converter.json.MappingJackson2HttpMessageConverter;
import org.springframework.stereotype.Service;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.client.RestClientException;
import org.springframework.web.client.RestTemplate;
import org.springframework.beans.factory.annotation.Value;
import java.net.URLDecoder;
import java.nio.charset.StandardCharsets;
import java.util.Arrays;
import java.util.Collections;
import java.util.HashMap;
import java.util.Map;
import java.util.stream.Collectors;

@Service
@Slf4j
public class OAuthService {
    @Value("${spring.security.oauth2.client.registration.github.client-id}")
    private String clientId;

    @Value("${spring.security.oauth2.client.registration.github.client-secret}")
    private String clientSecret;

    public String getAccessToken(String code) throws RestClientException {

        System.out.println("code : " + code);
        RestTemplate restTemplate = new RestTemplate();
        HttpHeaders headers = new HttpHeaders();
        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
        MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
        map.add("client_id", clientId);
        map.add("client_secret", clientSecret);
        map.add("code", code);
        HttpEntity<MultiValueMap<String, String>> entity = new HttpEntity<>(map, headers);
        ResponseEntity<String> response =
                restTemplate.postForEntity("https://github.com/login/oauth/access_token", entity, String.class);
        System.out.println("response : " + response.getBody());
        return response.getBody();

    }

//        // 인증 코드를 사용하여 Access Token 요청
//        RestTemplate restTemplate = new RestTemplate(Arrays.asList(
//                new FormHttpMessageConverter(),
//                new MappingJackson2HttpMessageConverter()));
//        HttpHeaders headers = new HttpHeaders();
//        headers.setContentType(MediaType.APPLICATION_FORM_URLENCODED);
//        MultiValueMap<String, String> map = new LinkedMultiValueMap<>();
//        map.add("client_id", clientId);
//        map.add("client_secret", clientSecret);
//        map.add("code", code);
//
//        HttpEntity<MultiValueMap<String, String>> entity = new HttpEntity<>(map, headers);
//
//        ResponseEntity<String> response =
//                restTemplate.postForEntity("https://github.com/login/oauth/access_token", entity, String.class);
//        log.info("GitHub Response: {}", response.getBody());
//        // GitHub로부터 받은 응답에서 access_token 추출
//        return extractToken(response.getBody());
//    }
//    private String extractToken(String body) {
//        String decodedBody = URLDecoder.decode(body, StandardCharsets.UTF_8);
//        Map<String, String> params = Arrays.stream(decodedBody.split("&"))
//                .map(param -> param.split("="))
//                .collect(Collectors.toMap(
//                        e -> e[0],
//                        e -> e.length > 1 ? e[1] : "")); // 배열 길이 확인
//
//        if (params.containsKey("access_token")) {
//            log.info("Access token: {}", params.get("access_token"));
//            return params.get("access_token");
//        } else {
//            // 적절한 예외 처리 또는 오류 로깅
//            throw new IllegalStateException("Access token not found in response");
//        }
//    }
//    public GithubUser getUserInfo(String accessToken) throws RestClientException {
//        RestTemplate restTemplate = new RestTemplate();
//        HttpHeaders headers = new HttpHeaders();
//        headers.setAccept(Collections.singletonList(MediaType.APPLICATION_JSON));
//        headers.setBearerAuth(accessToken);
//
//        HttpEntity<String> entity = new HttpEntity<>("parameters", headers);
//
//        ResponseEntity<GithubUser> response = restTemplate.exchange("https://api.github.com/user", HttpMethod.GET, entity, GithubUser.class);
//
//        return response.getBody();
//    }
}
//import lombok.extern.slf4j.Slf4j;
//import org.springframework.beans.factory.annotation.Value;
//import org.springframework.http.*;
//import org.springframework.stereotype.Service;
//import org.springframework.web.reactive.function.client.WebClient;
//import com.example.taba.model.GithubUser;
//import org.springframework.web.client.RestClientException;
//
//import java.net.URLDecoder;
//import java.nio.charset.StandardCharsets;
//import java.util.Arrays;
//import java.util.HashMap;
//import java.util.Map;
//import java.util.stream.Collectors;
//
//@Service
//@Slf4j
//public class OAuthService {
//
//    @Value("${spring.security.oauth2.client.registration.github.client-id}")
//    private String clientId;
//
//    @Value("${spring.security.oauth2.client.registration.github.client-secret}")
//    private String clientSecret;
//
//    public String getAccessToken(String code) throws RestClientException {
//        WebClient webClient = WebClient.create();
//        String response = webClient.post()
//                .uri("https://github.com/login/oauth/access_token")
//                .header(HttpHeaders.CONTENT_TYPE, MediaType.APPLICATION_JSON_VALUE)
//                .bodyValue(buildAccessTokenRequest(code))
//                .retrieve()
//                .bodyToMono(String.class)
//                .block();
//
//        return extractToken(response);
//    }
//
//    private String extractToken(String body) {
//        String decodedBody = URLDecoder.decode(body, StandardCharsets.UTF_8);
//        Map<String, String> params = Arrays.stream(decodedBody.split("&"))
//                .map(param -> param.split("="))
//                .collect(Collectors.toMap(
//                        e -> e[0],
//                        e -> e.length > 1 ? e[1] : ""
//                ));
//
//        if (params.containsKey("access_token")) {
//            return params.get("access_token");
//        } else {
//            throw new RestClientException("Access token not found in response");
//        }
//    }
//
//    public GithubUser getUserInfo(String accessToken) throws RestClientException {
//        WebClient webClient = WebClient.create();
//        return webClient.get()
//                .uri("https://api.github.com/user")
//                .header(HttpHeaders.AUTHORIZATION, "Bearer " + accessToken)
//                .retrieve()
//                .bodyToMono(GithubUser.class)
//                .block();
//    }
//
//    private Map<String, Object> buildAccessTokenRequest(String code) {
//        Map<String, Object> map = new HashMap<>();
//        map.put("client_id", clientId);
//        map.put("client_secret", clientSecret);
//        map.put("code", code);
//        return map;
//    }
//}
