import { HttpClient } from '@angular/common/http';
import { Injectable, inject, signal } from '@angular/core';
import { jwtDecode } from 'jwt-decode';
import { catchError } from 'rxjs';
import { environment } from '../../environments/environments';
import { UserInterface } from '../interfaces/user.interface';
@Injectable({
  providedIn: 'root',
})
export class AuthService {
  http = inject(HttpClient);
  apiUrl: string = environment.apiUrl;
  currentUserSig = signal<UserInterface | undefined | null>(undefined);
  accessToken = signal<string | undefined | null>(undefined);

  async isTokenExpired(): Promise<boolean> {
    let expired: boolean = true;
    if (!this.accessToken()) {
      try {
        const response: any = await this.http
          .post(
            `${this.apiUrl}/refresh`,
            {},
            {
              headers: {
                'Access-Control-Allow-Origin': 'http://localhost:4200',
              },
              withCredentials: true,
            }
          )
          .pipe(
            catchError((error) => {
              console.log(error);

              return '';
            })
          )
          .toPromise();
        this.accessToken.set(response.access_token);
      } catch (err) {
        expired = true;
      }
    }

    const token = this.accessToken();
    if (token) {
      try {
        let decoded: any = jwtDecode(token);
        if (decoded.exp < Date.now() / 1000) {
          try {
            const response: any = await this.http
              .post(
                `${this.apiUrl}/refresh`,
                {},
                {
                  headers: {
                    'Access-Control-Allow-Origin':
                      'https://http://localhost:4200',
                  },
                  withCredentials: true,
                }
              )
              .pipe(
                catchError((error) => {
                  console.log(error);

                  return '';
                })
              )
              .toPromise();

            this.accessToken.set(response.access_token);
            expired = false;
          } catch (err) {
            expired = true;
          }
        } else {
          expired = decoded.exp < Date.now() / 1000;
        }
      } catch (err) {
        expired = true;
      }
    }

    return expired;
  }
}
