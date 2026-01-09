import { Injectable } from '@angular/core';
import { HttpClient } from '@angular/common/http';
import { Observable } from 'rxjs';

interface QueryResponse {
  result: any;
}

@Injectable({
  providedIn: 'root'
})
export class ApiService {
  private apiUrl = '/api/query';

  constructor(private http: HttpClient) {}

  getSimScore(query: string): Observable<QueryResponse> {
    return this.http.post<QueryResponse>(this.apiUrl, { query });
  }
}