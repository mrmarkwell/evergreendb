import { BrowserModule } from '@angular/platform-browser';
import { NgModule } from '@angular/core';
import {
    MatNativeDateModule,
    MatIconModule,
    MatSidenavModule,
    MatButtonModule,
    MatCardModule,
    MatChipsModule
} from '@angular/material';

import { HttpClientModule } from '@angular/common/http'

import { BrowserAnimationsModule } from '@angular/platform-browser/animations';
import { DatePipe } from '@angular/common';

import { RestService } from './rest.service';
import { AppComponent } from './app.component';
import { AppRoutingModule } from './app-routing.module';
import { CalendarModule } from './calendar/calendar.module';
import { ChildrenModule } from './children/children.module';
import { RemindersModule } from './reminders/reminders.module';
import { SettingsModule } from './settings/settings.module';

import { MAT_MOMENT_DATE_FORMATS, MomentDateAdapter } from '@angular/material-moment-adapter';
import { DateAdapter, MAT_DATE_FORMATS, MAT_DATE_LOCALE } from '@angular/material/core';

@NgModule({
    declarations: [
        AppComponent
    ],
    imports: [
        BrowserModule,
        AppRoutingModule,
        HttpClientModule,
        MatNativeDateModule,
        MatIconModule,
        MatSidenavModule,
        MatButtonModule,
        BrowserAnimationsModule,
        CalendarModule,
        ChildrenModule,
        RemindersModule,
        SettingsModule,
        MatCardModule,
        MatChipsModule
    ],
    providers: [
        RestService,
        DatePipe,
       
        { provide: MAT_DATE_LOCALE, useValue: 'zh_CN' },
        { provide: DateAdapter, useClass: MomentDateAdapter, deps: [MAT_DATE_LOCALE] },
        { provide: MAT_DATE_FORMATS, useValue: MAT_MOMENT_DATE_FORMATS },
    ],
    bootstrap: [AppComponent]
})
export class AppModule { }
