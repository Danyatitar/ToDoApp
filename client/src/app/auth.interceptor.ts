import { HttpInterceptorFn } from '@angular/common/http';
import { inject } from '@angular/core';
import { AuthService } from './services/auth.service';
export const authInterceptor: HttpInterceptorFn = (request, next) => {
  const authService = inject(AuthService);

  request = request.clone({
    withCredentials: true,
    setHeaders: {
      Authorization: authService.accessToken()
        ? `Bearer ${authService.accessToken()}`
        : '',
    },
  });

  return next(request);
};
