import { Injectable, EventEmitter } from '@angular/core';
//import { HttpClient, Headers } from '@angular/http';
import { HttpClient, HttpHeaders } from '@angular/common/http'
import 'rxjs/add/operator/toPromise';

import { Child } from './child';
import { ChildPhoto } from './child-photo'
import { Interaction } from './interaction';
import { Reminder } from './reminder';
import { FamilyMember } from './family-member';
import { ProjectedPathway } from './projected-pathway';

@Injectable()
export class RestService {
    changeEmitter: EventEmitter<any> = new EventEmitter();
    constructor(private http: HttpClient) {
        this.refreshOrResetAllCaches();
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

    // Opportunistic caching of retrieved data
    private getAndCacheProjectedPathways(child_id: number): Promise<ProjectedPathway[]> {
        return this.getEntity('fss_projected_pathway', `child_id=${child_id}`).then(results => {
            this.projected_pathways_cache.set(child_id, results);
            return results as ProjectedPathway[];
        });
    }

    // Opportunistic caching of retrieved data
    private getAndCacheInteractions(child_id: number): Promise<Interaction[]> {
        return this.getEntity('fss_interaction', `child_id=${child_id}`).then(results => {
            this.interactions_cache.set(child_id, results);
            return results as Interaction[];
        });
    }

    // Opportunistic caching of retrieved data
    private getAndCacheFamilyMembers(child_id: number): Promise<FamilyMember[]> {
        return this.getEntity('fss_family_member', `child_id=${child_id}`).then(results => {
            this.family_members_cache.set(child_id, results);
            return results as FamilyMember[]
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
        let url = `${this.evergreenUrl}/entity/${type}`;
        if (query) { url = url + '?' + query };
        return this.http.get(url)
            .toPromise().then(response => response)
            .catch(this.handleError);
    }

    private addEntity(type: string, entity: any): Promise<any> {
        let url = `${this.evergreenUrl}/entity/${type}`;
        return this.http.post(url, JSON.stringify(entity), { headers: this.headers })
            .toPromise().then(res => { this.refresh(); return res; })
            .catch(this.handleError);
    }

    private updateEntity(type: string, entity: any): Promise<any> {
        const url = `${this.evergreenUrl}/entity/${type}?id=${entity.id}`;
        return this.http.put(url, JSON.stringify(entity), { headers: this.headers })
            .toPromise().then(res => { this.refresh(); return res; })
            .catch(this.handleError);
    }

    private deleteEntity(type: string, id: number): Promise<void> {
        const url = `${this.evergreenUrl}/entity/${type}?id=${id}`;
        return this.http.delete(url, { headers: this.headers })
            .toPromise().then(() => { this.refresh(); return null }).catch(this.handleError);
    }

    getEnum(field: string): Promise<string[]> {
        let url = `${this.evergreenUrl}/enum/${field}`;
        return this.http.get(url)
            .toPromise().then(response => response)
            .catch(this.handleError);
    }

    getInteractionFiles(interaction_id: number): Promise<String[]> {
        let url = `${this.evergreenUrl}/interactionfiles/${interaction_id}`;
        return this.http.get(url).toPromise().then(response => response).catch(this.handleError);
    }

    deleteInteractionFile(interaction_id: number, filenames: String []): Promise<any> {
        let url = `${this.evergreenUrl}/interactionfiles/${interaction_id}`;
        return this.http.post(url, JSON.stringify(filenames), { headers: this.headers })
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
            return results as FamilyMember
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
    getDateFromString(date_string: string): Date {
        if (date_string == null || date_string.length == 0) return null;
        return new Date(date_string.replace(/-/g, '\/').replace(/T.+/, ''));
    }

    // Utility function for creating a string from a Date object.
    getStringFromDate(date_obj: Date): string {
        if (date_obj) {
            let day = date_obj.getDate();
            let month = date_obj.getMonth() + 1;
            let year = date_obj.getFullYear();
            let date_string = year + "-" + month + "-" + day;

            return date_string;
        }
        else {
            return "";
        }
    }

    //File uploader needs the photo upload
    getPhotoUploadUrl(): string {
        return this.evergreenUrl + "/upload";
    }
    getChildPhotoUrl(id: number): string {
        return `${this.evergreenUrl}/static/photos/child${id}.jpeg`;
    }

    getInteractionFileDownloadUrl(id: number, filename: string): string {
        return `${this.evergreenUrl}/static/interactions/${id}/${filename}`
    }
    
    private handleError(error: any): Promise<any> {
        console.error('An error occurred', error);
        return Promise.reject(error.message || error);
    }

    getBaseUrl(): String{
        return this.evergreenUrl;
    }

    private evergreenUrl = 'http://127.0.0.1:5000';
    // private evergreenUrl = "http://ec2-54-193-44-138.us-west-1.compute.amazonaws.com";
    private headers = new HttpHeaders({ 'Content-Type': 'application/json' });
}
