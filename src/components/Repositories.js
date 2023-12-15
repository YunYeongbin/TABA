import React, { useState, useEffect } from 'react';
import axios from 'axios';

function Repositories() {
  const [repos, setRepos] = useState([]);

  useEffect(() => {
    const fetchRepos = async () => {
      try {
        const response = await axios.get('http://localhost:8080/api/repositories'); // 백엔드 엔드포인트 URL로 변경
        setRepos(response.data);
      } catch (error) {
        console.error('Error fetching repositories', error);
      }
    };

    fetchRepos();
  }, []);

  return (
    <div>
      <h1>GitHub Repositories</h1>
      <ul>
        {repos.map(repo => (
          <li key={repo.id}>{repo.name}</li> // 예시이므로 'id'와 'name'이 실제 데이터 필드와 다를 수 있음
        ))}
      </ul>
    </div>
  );
}

export default Repositories;