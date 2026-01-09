import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

@Component({
  selector: 'app-chat',
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class ChatComponent {
  userInput: string = '';
  result: any = null;
  isLoading: boolean = false;
  error: string = '';

  constructor(private apiService: ApiService, private cdr: ChangeDetectorRef) {}

  sendMessage() {
    if (this.userInput.trim()) {
      this.isLoading = true;
      this.error = '';
      
      console.log('Sending query:', this.userInput);
      
      this.apiService.getSimScore(this.userInput).subscribe({
        next: (response) => {
          console.log('Full response:', response);
          console.log('Result:', response.result);
          this.result = response.result;
          this.isLoading = false;
          this.cdr.detectChanges(); // Force Angular to update the view
          console.log('isLoading set to false, result:', this.result);
        },
        error: (err) => {
          console.error('API Error:', err);
          this.error = 'Failed to get results: ' + (err.error?.detail || err.message);
          this.isLoading = false;
        },
        complete: () => {
          console.log('Observable completed');
        }
      });
      
      // Clear input after sending
      this.userInput = '';
    }
  }
}