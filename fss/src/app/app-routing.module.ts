import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { LoginPage } from './login/login-page.component';
import { ChildrenPage } from './children/children-page.component';
import { RemindersTab } from './reminders/reminders-tab.component';
import { CalendarTab } from './calendar/calendar-tab.component';
import { SettingsPage } from './settings/settings-page.component';
import { AdminPage } from './settings/admin-settings-page.component';
import { AuthGuard } from './login/auth-guard'
import { AdminAuthGuard } from './login/admin-auth-guard'


const routes : Routes = [
	{ path: '', redirectTo:'/login', pathMatch:'full'},
	{ path: 'children', component: ChildrenPage, canActivate: [AuthGuard]},
	{ path: 'reminders', component: RemindersTab, canActivate: [AuthGuard] },
	{ path: 'calendar', component: CalendarTab, canActivate: [AuthGuard] },
    { path: 'settings', component: SettingsPage, canActivate: [AuthGuard] },
    { path: 'admin', component: AdminPage, canActivate: [AdminAuthGuard] },
    { path: 'login', component: LoginPage }
]

@NgModule({
    imports: [RouterModule.forRoot(routes)],
    providers: [AuthGuard, AdminAuthGuard],
	exports: [RouterModule]
})
export class AppRoutingModule {}
