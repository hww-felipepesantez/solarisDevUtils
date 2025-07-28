///coastal_road/environ/scatter/**

int n = usd_attriblen(0, @primpath, "positions");

vector pos[] = usd_attrib(0, @primpath, "positions");

string campath = chs("camera"); 
matrix mcam = usd_worldtransform(0, campath);
float focal = usd_attrib(0, campath, "focalLength");
float hap = usd_attrib(0, campath, "horizontalAperture");
float vap = usd_attrib(0, campath, "verticalAperture");
vector2 clipping = usd_attrib(0, campath, "clippingRange");
float near = clipping.x;
float far = clipping.y;

float o = chf("overscan"); 

for(int i=0; i<n; i++){
    vector pcam = pos[i] * invert(mcam);
    float cambackup = o*chf("cam_z_depth");
    
    pcam.z -= cambackup; 
    
    float xclip = focal * pcam.x / (hap/2);
    float yclip = focal * pcam.y / (vap/2);
    float wclip = pcam.z;
    
    float ndcx = xclip / wclip;
    float ndcy = yclip / wclip;
    
    if(-pcam.z < near || -pcam.z > far-cambackup) append(i[]@invisibleIds, i);
    if(ndcx+o < -1 || ndcx-o > 1 || ndcy+o < -1 || ndcy-o > 1) append(i[]@invisibleIds, i);
}