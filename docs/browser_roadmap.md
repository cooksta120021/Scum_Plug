## **Key Features & Implementation Details**  

### **1. Roles & Permissions System**
- **Creator** → Full control over their squad/group. Approves new members, deletes posts, and removes members.  
- **Member** → Can post and comment but cannot delete or manage others' content.  
- **Admin** → No restrictions. Can create/manage anything, force-remove users, and delete any post.  
- **Co-Leaders (Moderators) (Optional, Future Feature)** → A creator may assign moderators to help with approvals and post management.  

### **2. Squad vs. Group Rules**
- **Users can only be in ONE squad at a time**.  
- **Users can be in up to 3 groups.**  
- **Leaving is allowed freely, but rejoining requires approval.**  

### **3. User Invitation System**
- **Users must request to join squads/groups**.  
- **Squads & groups are publicly visible**, but **content and members are private** until approved.  
- **Only approved users can see members & posts.**  

### **4. Archive (Post) Visibility**
- **All squad/group posts are private** (visible only to members).  
- **Users must be in the group to see posts/members.**  

### **5. Online Status**
- Users manually **toggle an "Online/Offline" switch** to show their active status.  
- **Firestore stores a timestamp of the last toggle.**  

### **6. Photo Uploads**
- **Users can upload a maximum of 2 photos** (stored as **base64**).  
- **Compression will be extreme to save storage.**  
- **Users can delete a photo to upload a new one.**  
- **Admins have unlimited uploads & full control over all photos.**  

### **7. Admin Abilities**
- Admins can **delete posts, remove users, and approve or reject squad/group members**.  
- Admins can **override any approval process**.  
- Admins can **upload unlimited photos**.  

### **8. Notifications & Activity Logs**
- **Users receive notifications when their join request is approved/rejected.**  
- **No activity log is required for now.**  

---

## **Firestore Database Structure**  

### **Users Collection (`users/`)**  
```json
{
  "id": "UID",
  "username": "string",
  "email": "string",
  "squad_id": "squadID | null",
  "group_ids": ["groupID1", "groupID2", "groupID3"],
  "photos": ["base64String1", "base64String2"],
  "last_active": "timestamp",
  "is_admin": true/false,
  "is_online": true/false
}
```

### **Squads Collection (`squads/`)**  
```json
{
  "id": "squadID",
  "name": "string",
  "server_name": "string",
  "creator_id": "UID",
  "member_ids": ["UID1", "UID2"],
  "pending_requests": ["UID3", "UID4"],
  "archives": "subcollection"
}
```

### **Groups Collection (`groups/`)**  
```json
{
  "id": "groupID",
  "name": "string",
  "server_name": "string",
  "creator_id": "UID",
  "member_ids": ["UID1", "UID2"],
  "pending_requests": ["UID3", "UID4"],
  "archives": "subcollection"
}
```

### **Archives Collection (`squads/{squadId}/archives/` & `groups/{groupId}/archives/`)**  
```json
{
  "id": "archiveID",
  "title": "string",
  "content": "string",
  "timestamp": "timestamp",
  "author_id": "UID"
}
```

### **Comments Collection (`archives/{archiveId}/comments/`)**  
```json
{
  "id": "commentID",
  "content": "string",
  "timestamp": "timestamp",
  "author_id": "UID"
}
```

