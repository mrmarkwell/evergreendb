import { Injectable, EventEmitter } from '@angular/core';
//import { HttpClient, Headers } from '@angular/http';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import 'rxjs/add/operator/toPromise';

import * as moment from 'moment';

import { Child } from './child';
import { User } from './user';
import { ChildPhoto } from './child-photo'
import { Interaction } from './interaction';
import { Reminder } from './reminder';
import { FamilyMember } from './family-member';
import { ProjectedPathway } from './projected-pathway';
import { Settings } from './settings'

@Injectable()
export class RestService {
    changeEmitter: EventEmitter<any> = new EventEmitter();
    settings: Settings = new Settings();
    constructor(private http: HttpClient) {
        this.refreshOrResetAllCaches();
        this.settings.save_notify_interval = 1000;
        this.settings.current_username = "";
        this.settings.current_password = "";
        this.settings.setDevMode(false);
    }

    // Caches for performance improvement.
    private children_cache: Map<number, any> = new Map<number, any>();
    private interactions_cache: Map<number, any> = new Map<number, any>();
    private family_members_cache: Map<number, any> = new Map<number, any>();
    private projected_pathways_cache: Map<number, any> = new Map<number, any>();

    // Called when the refresh button is clicked, or when any PUT, POST, or DELETE goes to the backend.
    private refreshOrResetAllCaches(): Promise<Child[]> {
        this.children_cache.clear();
        this.interactions_cache.clear();
        this.family_members_cache.clear();
        this.projected_pathways_cache.clear();
        // Fill the children cache immediately. The others will populate on demand.
        return this.getEntity('fss_child').then(results => {
            let ret = results.map(child => {
                let the_child = new Child(child);
                this.children_cache.set(the_child.id, child);
                return the_child;
            });
            return ret;
        });
    }

    public checkLogin(password?: string): Promise<boolean> {
        let url = `${this.getBaseUrl()}/authcheck`;
        return this.http.get(url, { headers: this.getHeaders(password) })
            .toPromise().then(response => { return true })
            .catch(error => { return false });
    }

    public addUser(user: User): Promise<boolean> {
        let url = `${this.getBaseUrl()}/user`;
        return this.http.post(url, JSON.stringify(user), { headers: this.getHeaders() })
        .toPromise().then(response => { return true })
        .catch(error => { return false });
    }

    public checkAdminLogin(): Promise<boolean> {
        let url = `${this.getBaseUrl()}/adminauthcheck`;
        return this.http.get(url, { headers: this.getHeaders() })
            .toPromise().then(response => { return true })
            .catch(error => { return false });
    }

    public changePassword(new_password: string): Promise<boolean> {
        return this.getCurrentUserId().then(id => {
            let url = `${this.getBaseUrl()}/user?id=${id}`;
            let user = new User();
            user.username = this.settings.current_username;
            user.password = new_password;
            return this.http.put(url, JSON.stringify(user), {headers: this.getHeaders()})
            .toPromise()
            .then(response => { this.settings.current_password = new_password; return true; })
            .catch(error => { return false });
        })
    }

    public getCurrentUserId(): Promise<number> {
        let url = `${this.getBaseUrl()}/user?username=${this.settings.current_username}`;
        return this.http.get(url, { headers: this.getHeaders() })
        .toPromise().then(response => { console.log(response); return response[0]["id"]; }).catch(this.handleError);
    }

    private getHeaders(password?: string): HttpHeaders {
        return new HttpHeaders({ 'Content-Type': 'application/json',
    "Authorization": "Basic " + btoa(this.settings.current_username + ":" + (password ? password : this.settings.current_password)) });
    }
    // Opportunistic caching of retrieved data
    private getAndCacheProjectedPathways(child_id: number): Promise<ProjectedPathway[]> {
        return this.getEntity('fss_projected_pathway', `child_id=${child_id}`).then(results => {
						let projected_pathways = results.map(projected_pathway => {
								return new ProjectedPathway(projected_pathway);
						});
            this.projected_pathways_cache.set(child_id, projected_pathways);
            return projected_pathways;
        });
    }

    // Opportunistic caching of retrieved data
    private getAndCacheInteractions(child_id: number): Promise<Interaction[]> {
        return this.getEntity('fss_interaction', `child_id=${child_id}`).then(results => {
						let interactions = results.map(interaction => {
								return new Interaction(interaction);
						});
            this.interactions_cache.set(child_id, interactions);
            return interactions;
        });
    }

    // Opportunistic caching of retrieved data
    private getAndCacheFamilyMembers(child_id: number): Promise<FamilyMember[]> {
        return this.getEntity('fss_family_member', `child_id=${child_id}`).then(results => {
            let family_members = results.map(family_member => {
                return new FamilyMember(family_member);
            });
            this.family_members_cache.set(child_id, family_members);
            return family_members;
        });
    }

    // Retrieve the children from the cache.
    private getCachedChildren(): Promise<Child[]> {
        let children = new Array<Child>();
        this.children_cache.forEach((value, key, map) => children.push(new Child(value)));
        return Promise.resolve(children);
    }

    // Retrieve a single cached child.
    private getCachedChild(child_id: number): Promise<Child> {
        return Promise.resolve(new Child(this.children_cache.get(child_id)));
    }

    // Global refresh. Resets caches and then causes ngOnChanges to be called everywhere.
    refresh(): void {
        this.refreshOrResetAllCaches().then(children => this.changeEmitter.emit());
    }

    //***** Generic functions *****//
    private getEntity(type: string, query?: string): Promise<any> {
        let url = `${this.getBaseUrl()}/entity/${type}`;
        if (query) { url = url + '?' + query };
        return this.http.get(url, { headers: this.getHeaders() })
            .toPromise().then(response => response)
            .catch(this.handleError);
    }

    private addEntity(type: string, entity: any): Promise<any> {
        let url = `${this.getBaseUrl()}/entity/${type}`;
        return this.http.post(url, JSON.stringify(entity), { headers: this.getHeaders() })
            .toPromise().then(res => { this.refresh(); return res; })
            .catch(this.handleError);
    }

    private updateEntity(type: string, entity: any): Promise<any> {
        const url = `${this.getBaseUrl()}/entity/${type}?id=${entity.id}`;
        return this.http.put(url, JSON.stringify(entity), { headers: this.getHeaders() })
            .toPromise().then(res => { this.refresh(); return res; })
            .catch(this.handleError);
    }

    private deleteEntity(type: string, id: number): Promise<void> {
        const url = `${this.getBaseUrl()}/entity/${type}?id=${id}`;
        return this.http.delete(url, { headers: this.getHeaders() })
            .toPromise().then(() => { this.refresh(); return null }).catch(this.handleError);
    }

    getEnum(field: string): Promise<string[]> {
        let url = `${this.getBaseUrl()}/enum/${field}`;
        return this.http.get(url)
            .toPromise().then(response => response)
            .catch(this.handleError);
    }

    getInteractionFiles(interaction_id: number): Promise<String[]> {
        let url = `${this.getBaseUrl()}/interactionfiles/${interaction_id}`;
        return this.http.get(url).toPromise().then(response => response).catch(this.handleError);
    }

    deleteInteractionFile(interaction_id: number, filenames: String[]): Promise<any> {
        let url = `${this.getBaseUrl()}/interactionfiles/${interaction_id}`;
        return this.http.post(url, JSON.stringify(filenames), { headers: this.getHeaders() })
            .toPromise().then(res => { this.refresh(); return res; })
            .catch(this.handleError);
    }

    // Child functions
    getChildren(): Promise<Child[]> {
        if (this.children_cache.size == 0) {
            return this.refreshOrResetAllCaches();
        }
        return this.getCachedChildren();
    }

    getChild(child_id: number): Promise<Child> {
        if (this.children_cache.size == 0) {
            return this.refreshOrResetAllCaches().then(children => children.find(child => child.id == child_id));
        }
        return this.getCachedChild(child_id);
    }
    addChild(child: Child): Promise<Child> {
        return this.addEntity('fss_child', child).then(results => results as Child);
    }
    updateChild(child: Child): Promise<Child> {
        return this.updateEntity('fss_child', child).then(results => results as Child);
    }
    deleteChild(id: number): Promise<void> {
        return this.deleteEntity('fss_child', id);
    }

    // Interactions, family members, and projected pathways are all pretty much the same except the url and return class
    getInteractions(child_id: number): Promise<Interaction[]> {
        if (this.interactions_cache.has(child_id)) {
            return Promise.resolve(this.interactions_cache.get(child_id) as Interaction[]);
        } else {
            return this.getAndCacheInteractions(child_id);
        }
    }

    getAllReminders(): Promise<Reminder[]> {
        let reminderList: Reminder[] = [];
        return this.getChildren().then(children => {
            return Promise.all(children.map((child, index, children) => {
                this.getInteractions(child.id).then(interactions =>
                    reminderList = reminderList.concat(interactions.map(interaction => new Reminder(interaction)))
                )
            })).then(() => Promise.resolve(reminderList))
        });
    }
    addInteraction(interaction: Interaction): Promise<Interaction> {
        return this.addEntity('fss_interaction', interaction).then(results => results as Interaction);
    }
    updateInteraction(interaction: Interaction): Promise<Interaction> {
        return this.updateEntity('fss_interaction', interaction).then(results => results as Interaction);
    }
    deleteInteraction(id: number): Promise<void> {
        return this.deleteEntity('fss_interaction', id);
    }

    getFamilyMembers(child_id: number): Promise<FamilyMember[]> {
        if (this.family_members_cache.has(child_id)) {
            return Promise.resolve(this.family_members_cache.get(child_id) as FamilyMember[]);
        } else {
            return this.getAndCacheFamilyMembers(child_id);
        }

    }
    addFamilyMember(family_member: FamilyMember): Promise<FamilyMember> {
        return this.addEntity('fss_family_member', family_member).then(results => {
            return new FamilyMember(results)
        });
    }
    updateFamilyMember(family_member: FamilyMember): Promise<FamilyMember> {
        return this.updateEntity('fss_family_member', family_member).then(results => results as FamilyMember);
    }
    deleteFamilyMember(id: number): Promise<void> {
        return this.deleteEntity('fss_family_member', id);
    }

    getProjectedPathway(child_id: number): Promise<ProjectedPathway[]> {
        if (this.projected_pathways_cache.has(child_id)) {
            return Promise.resolve(this.projected_pathways_cache.get(child_id) as ProjectedPathway[]);
        } else {
            return this.getAndCacheProjectedPathways(child_id);
        }
    }
    addProjectedPathway(projected_pathway: ProjectedPathway): Promise<ProjectedPathway> {
        return this.addEntity('fss_projected_pathway', projected_pathway).then(results => results as ProjectedPathway);
    }
    updateProjectedPathway(projected_pathway: ProjectedPathway): Promise<ProjectedPathway> {
        return this.updateEntity('fss_projected_pathway', projected_pathway).then(results => results as ProjectedPathway);
    }
    deleteProjectedPathway(id: number): Promise<void> {
        return this.deleteEntity('fss_projected_pathway', id);
    }

    // Utility function for creating Date objects from strings for binding to datepickers.
    getDateFromString(date_string: string): moment.Moment {
        let date = moment(date_string, "YYYY-MM-DD");
        if (date.isValid()) {
            return date;
        } else {
            return null;
        }
    }

    // Utility function for creating a string from a Date object.
    getStringFromDate(date_obj: moment.Moment): string {
        if (date_obj && date_obj.isValid()) {
            return date_obj.format("YYYY-MM-DD");
        }
        else {
            return null;
        }
    }

    //File uploader needs the photo upload
    getPhotoUploadUrl(): string {
        return this.getBaseUrl() + "/upload";
    }
    getChildPhotoUrl(id: number): string {
        return `${this.getBaseUrl()}/static/photos/child${id}.jpeg`;
    }

    getInteractionFileDownloadUrl(id: number, filename: string): string {
        return `${this.getBaseUrl()}/static/interactions/${id}/${filename}`
    }

    private handleError(error: any): Promise<any> {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }

    getBaseUrl(): String {
        return this.settings.evergreen_url;
    }

}
