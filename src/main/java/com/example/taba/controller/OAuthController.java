package com.example.taba.controller;

import com.example.taba.model.GithubUser;
import com.example.taba.model.OAuthInfo;

import com.example.taba.service.OAuthService;
import com.example.taba.service.UserService;

import jakarta.servlet.http.Cookie;
import jakarta.servlet.http.HttpServletResponse;
import lombok.AllArgsConstructor;
import lombok.RequiredArgsConstructor;
import org.springframework.beans.factory.annotation.Value;
import org.springframework.http.*;
import org.springframework.util.LinkedMultiValueMap;
import org.springframework.util.MultiValueMap;
import org.springframework.web.bind.annotation.*;
import org.springframework.web.client.RestTemplate;
import org.springframework.web.servlet.view.RedirectView;


//@CrossOrigin(origins = "*", allowedHeaders = "*")
@RestController
@RequiredArgsConstructor
public class OAuthController {
    @Value("${spring.security.oauth2.client.registration.github.client-id}")
    private String clientId;
    @Value("${spring.security.oauth2.client.registration.github.client-secret}")
    private String clientSecret;
    private UserService userService;

    @GetMapping("/oauth")
    public RedirectView handleGithubCallback(@RequestParam String code) {
        System.out.println("code : "+code);
        RestTemplate restTemplate = new RestTemplate();

        ResponseEntity<OAuthInfo> response = restTemplate.exchange("https://github.com/login/oauth/access_token",
                HttpMethod.POST,
                getAccessToken(code),
                OAuthInfo.class);
        String accessToken = response.getBody().getAccessToken();
        System.out.println("access token : "+accessToken);

        // 클라이언트로 리디렉션
        String redirectUrl = "http://localhost:3000/?accessToken=" + accessToken;
        return new RedirectView(redirectUrl);
    }
    private HttpEntity<MultiValueMap<String,String>> getAccessToken(String code) {
        MultiValueMap<String, String> params = new LinkedMultiValueMap<>();
        params.add("client_id",clientId);
        params.add("client_secret",clientSecret);
        params.add("code",code);

        HttpHeaders headers = new HttpHeaders();
        return new HttpEntity<>(params,headers);
    }

    private HttpEntity<MultiValueMap<String,String>> getUserInfo(String access_token) {
        HttpHeaders requestHeaders = new HttpHeaders();
        requestHeaders.add("Authorization", "token " + access_token);
        return new HttpEntity<>(requestHeaders);
    }
    @GetMapping("/api/repositories")
    public ResponseEntity<String> getUserRepositories(@RequestHeader("Authorization") String authorizationHeader) {
        try {
            String accessToken = authorizationHeader.substring("Bearer ".length());
            RestTemplate restTemplate = new RestTemplate();
            HttpHeaders headers = new HttpHeaders();
            headers.setBearerAuth(accessToken); // Bearer 토큰으로 인증
            HttpEntity<String> entity = new HttpEntity<>(headers);
            ResponseEntity<String> response = restTemplate.exchange(
                    "https://api.github.com/user/repos",
                    HttpMethod.GET,
                    entity,
                    String.class);
            return ResponseEntity.ok().body(response.getBody());
        } catch (Exception e) {
            // 예외 처리 로직 (에러 로그 기록, 적절한 HTTP 응답 반환 등)
            return ResponseEntity.status(HttpStatus.INTERNAL_SERVER_ERROR).body("Error retrieving repositories");
        }
    }
}
