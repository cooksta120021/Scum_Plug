## **Social Network Plugin Roadmap**

### **Current Implementation**
- Basic PyQt5-based social network interface
- Username input
- Post creation and display
- Logging functionality

### **Planned Features**
1. **User Authentication**
   - Implement login/signup functionality
   - Store user credentials securely
   - Add password hashing

2. **Enhanced Post Management**
   - Add timestamps to posts
   - Implement post editing and deletion
   - Add likes and comments functionality

3. **User Roles & Permissions**
   - Implement Creator, Member, and Admin roles
   - Add role-based access control
   - Create squad/group management system

4. **Media Support**
   - Allow photo uploads (max 2 photos per user)
   - Implement base64 photo storage
   - Add photo compression

5. **Notification System**
   - Implement join request notifications
   - Add real-time status updates

### **Technical Roadmap**
- [ ] Integrate with Firestore for backend
- [ ] Implement secure authentication
- [ ] Create comprehensive logging system
- [ ] Add unit and integration tests
- [ ] Optimize performance and memory usage

### **Design Considerations**
- Maintain clean, modular code structure
- Prioritize user privacy and data security
- Create intuitive and responsive UI
- Minimize external dependencies

### **Future Enhancements**
- Mobile app version
- End-to-end encryption
- Advanced search and filter capabilities
- Machine learning-based content recommendations

---

## **Next Steps**
1. **Set Up Firestore Security Rules**  
   - Prevent non-members from accessing squad/group data.  
   - Ensure only **creators** can manage squads/groups.  
   - Ensure only **admins** have full control.  

2. **Implement Join Requests System**  
   - Store **pending join requests** in each squad/group document.  
   - Allow **creators/admins to approve or deny** requests.  

3. **Create Real-Time Online Status System**  
   - Add **toggle switch for online/offline** status.  
   - Store **last_active timestamp** for tracking.  

4. **Develop UI for Creating & Managing Squads/Groups**  
   - Forms for **creating squads & groups** (including server name).  
   - Interfaces for **managing membership requests**.  


## firebase information
Project name
ScumPlug

Project ID 
scumplug-b8ebb

Project number 
667359956907

Web API Key 
AIzaSyB1_g8c7keHmc9PgRsJCnP6eOBjhpI2smM

Environment
This setting customizes your project for different stages of the app lifecycle

Environment type
Unspecified

Public settings
These settings control instances of your project shown to the public

Public-facing name 
project-667359956907

Support email 
cooksta120021@gmail.com