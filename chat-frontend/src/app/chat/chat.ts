import { Component, ChangeDetectorRef } from '@angular/core';
import { CommonModule } from '@angular/common';
import { FormsModule } from '@angular/forms';
import { ApiService } from '../services/api.service';

interface Message {
  text: string;
  timestamp: Date;
  sender: 'user' | 'system';
  sentimentScore?: number;
  color?: string;
}

@Component({
  selector: 'app-chat',
  imports: [CommonModule, FormsModule],
  templateUrl: './chat.html',
  styleUrl: './chat.css',
})
export class ChatComponent {
  userInput: string = '';
  messages: Message[] = [];
  isLoading: boolean = false;

  constructor(private apiService: ApiService, private cdr: ChangeDetectorRef) {}

  sendMessage() {
    if (this.userInput.trim()) {
      const messageText = this.userInput.trim();
      this.isLoading = true;

      // Get sentiment score from backend
      this.apiService.getSimScore(messageText).subscribe({
        next: (response) => {
          console.log('Result:', response.result);
          const sentimentScore = response.result;
          const color = this.mapSentimentToColor(sentimentScore);

          // Add message with sentiment color
          this.messages.push({
            text: messageText,
            timestamp: new Date(),
            sender: 'user',
            sentimentScore: sentimentScore,
            color: color
          });

          this.isLoading = false;
          this.cdr.detectChanges(); // Force change detection
          setTimeout(() => this.scrollToBottom(), 0);
        },
        error: (err) => {
          console.error('API Error:', err);
          
          // Still add the message but with neutral color on error
          this.messages.push({
            text: messageText,
            timestamp: new Date(),
            sender: 'user',
            sentimentScore: 0,
            color: this.mapSentimentToColor(0)
          });

          this.isLoading = false;
          this.cdr.detectChanges(); // Force change detection
          setTimeout(() => this.scrollToBottom(), 0);
        }
      });

      // Clear input
      this.userInput = '';
    }
  }

  /**
   * Maps sentiment score [-120, 120] to RGB color spectrum
   * -120 (most negative) → Red
   * 0 (neutral) → Green
   * 120 (most positive) → Purple/Violet
   */
  mapSentimentToColor(score: number): string {
    // Clamp score to valid range
    const clampedScore = Math.max(-120, Math.min(120, score));
    
    // Normalize to [0, 1] range
    const normalized = (clampedScore + 120) / 240;
    
    let r: number, g: number, b: number;

    if (normalized < 0.5) {
      // Red → Yellow → Green (negative to neutral)
      const t = normalized * 2; // 0 to 1
      
      if (t < 0.5) {
        // Red → Orange → Yellow
        const tt = t * 2; // 0 to 1
        r = 255;
        g = Math.round(165 * tt); // Ramp up green
        b = 0;
      } else {
        // Yellow → Green
        const tt = (t - 0.5) * 2; // 0 to 1
        r = Math.round(255 * (1 - tt)); // Ramp down red
        g = Math.round(165 + (90 * tt)); // Yellow green to pure green
        b = 0;
      }
    } else {
      // Green → Cyan → Blue → Purple (neutral to positive)
      const t = (normalized - 0.5) * 2; // 0 to 1
      
      if (t < 0.33) {
        // Green → Cyan
        const tt = t / 0.33; // 0 to 1
        r = 0;
        g = 255;
        b = Math.round(255 * tt); // Ramp up blue
      } else if (t < 0.67) {
        // Cyan → Blue
        const tt = (t - 0.33) / 0.34; // 0 to 1
        r = 0;
        g = Math.round(255 * (1 - tt)); // Ramp down green
        b = 255;
      } else {
        // Blue → Purple
        const tt = (t - 0.67) / 0.33; // 0 to 1
        r = Math.round(138 * tt); // Ramp up red for purple
        g = 0;
        b = 255;
      }
    }

    return `rgb(${r}, ${g}, ${b})`;
  }

  scrollToBottom() {
    const messageContainer = document.querySelector('.messages-container');
    if (messageContainer) {
      messageContainer.scrollTop = messageContainer.scrollHeight;
    }
  }

  formatTime(date: Date): string {
    return date.toLocaleTimeString('en-US', { 
      hour: 'numeric', 
      minute: '2-digit',
      hour12: true 
    });
  }

  getCurrentDate(): Date {
    return new Date();
  }
}