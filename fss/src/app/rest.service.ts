import {Injectable} from '@angular/core';
import {Http, Headers} from '@angular/http';
import 'rxjs/add/operator/toPromise';

import { Child } from './child';
import { Interaction } from './interaction';
import { FamilyMember } from './family-member';
import { ProjectedPathway } from './projected-pathway';

@Injectable()
export class RestService {
	constructor(private http: Http) {}

	getEntity(type: string, query?:string): Promise<any> {
		let url = `${this.evergreenUrl}/entity/${type}`;
		if (query) {url = url + '?' + query};
		return this.http.get(url)
			.toPromise().then(response => response.json())
			.catch(this.handleError);
	}
	addEntity(type: string, entity: any): Promise<any> {
		let url = `${this.evergreenUrl}/entity/${type}`;
		return this.http.post(url, JSON.stringify(entity), {headers: this.headers})
			.toPromise().then(res => res.json().data)
			.catch(this.handleError);
	}
	updateEntity(type:string, entity: any): Promise<any> {
		const url = `${this.evergreenUrl}/entity/${type}?id=${entity.id}`;
		return this.http.put(url, JSON.stringify(entity), {headers: this.headers})
			.toPromise().then(res => res.json().data)
			.catch(this.handleError);
	}
	deleteEntity(type: string, id: number): Promise<void> {
		const url = `${this.evergreenUrl}/entity/${type}?id=${id}`;
		return this.http.delete(url, {headers: this.headers})
			.toPromise().then( () => null ).catch(this.handleError);
	}

	getEnum(field: string): Promise<string[]> {
		let url = `${this.evergreenUrl}/enum/${field}`;
		return this.http.get(url)
			.toPromise().then(response => response.json())
			.catch(this.handleError);
	}

	getInteractions(child_id: number): Promise<Interaction[]> {
		return this.getEntity('fss_interaction',`child_id=${child_id}`).then( results => results as Interaction[] );
	}
	getFamilyMembers(child_id: number): Promise<FamilyMember[]> {
		return this.getEntity('fss_family_member',`child_id=${child_id}`).then( results => results as FamilyMember[] );
	}
	getProjectedPathway(child_id: number): Promise<ProjectedPathway[]> {
		return this.getEntity('fss_projected_pathway',`child_id=${child_id}`).then( results => results as ProjectedPathway[] );
	}

	getChildren(refresh: boolean = true): Promise<Child[]> {
		if (refresh || !this.childrenCache) {
			return this.getEntity('fss_child').then( results => this.childrenCache = results as Child[] );
		} else {
			return new Promise( (resolve,reject) => resolve(this.childrenCache) );
		}
	}
	getChild(child_id: number): Promise<Child> {
		return this.getChildren(false).then(children => children.find(child => child.id === child_id))
	}
	addChild(child: Child): Promise<Child> {
		return this.addEntity('fss_child', child).then(results => results as Child);
	}
	updateChild(child: Child): Promise<Child> {
		return this.updateEntity('fss_child', child).then(results => results as Child);
	}
	deleteChild(id: number): Promise<void> {
		return this.deleteEntity('fss_child',id);
	}

	private handleError(error: any): Promise<any> {
		console.error('An error occurred', error);
		return Promise.reject(error.message || error);
	}

	private evergreenUrl = 'http://127.0.0.1:5000';
	private headers = new Headers({'Content-Type': 'application/json'});
	private childrenCache: Child[];
}
