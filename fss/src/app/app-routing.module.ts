import { NgModule } from '@angular/core';
import { RouterModule, Routes } from '@angular/router';

import { ChildrenTab } from './children/children-tab.component';
import { RemindersTab } from './reminders/reminders-tab.component';

const routes : Routes = [
	{ path: '', redirectTo:'reminders', pathMatch:'full' },
	{ path: 'children', component: ChildrenTab },
	{ path: 'reminders', component: RemindersTab },
	{ path: 'calendar', component: ChildrenTab },
]

@NgModule({
	imports: [RouterModule.forRoot(routes)],
	exports: [RouterModule]
})
export class AppRoutingModule {}
