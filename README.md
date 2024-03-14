Пример использования

Регистрация:

```

curl -X POST http://localhost:8090/signup     -H "Content-Type: application/json"  
   -d '{"login": "newuser2", "password": "newpassword", "firstName": "gw", "lastName": "Doe", "birthDate": "1990-01-
01", "mail": "john.doe@example.com", "phoneNumber": "1234567890"}'
```

Проверка пароля

```
curl -X POST http://localhost:8090/login     -H "Content-Type: application/json"   
  -d '{"login": "newuser2", "password": "newpassword"}'
```

Обновление пароля

```
curl -X POST http://localhost:8090/update     -H "Content-Type: application/json"  -d '{"login": "newuser2", "password": "newpassword", "firstName": "gggg1", "lastName": "Doe", "birthDate": "1990-01-01", "mail": "john.doe@example.com", "phoneNumber": "1234567890"}'
```
