//**********************
// INCLUDED HEADER FILES
//**********************

#include <time.h>
#include <stdio.h>
#include <string.h>
#include <stdlib.h>
#include <malloc.h>
#include <conio.h>

//**********************
// FUNCTION PROTOTYPES
//**********************

void initialize(void);
void inputboxlist(void);
void execiterations(void);
void analyzebox (float hmx, float hy, float hmy, float hz, float hmz, float dim1, float dim2, float dim3);
void findsmallestz(void);
void checkfound(void);
void volumecheck(void);
void outputsolution(void);
void outputboxlist(void);
void report(void);

//********************************************************
// VARIABLE, CONSTANT AND STRUCTURE DECLARATIONS
//********************************************************

char strpx[10], strpy[10], strpz[10];
char strcox[10], strcoy[10], strcoz[10];
char strpackx[10], strpacky[10], strpackz[10];

char filename[12];
char strtemp[]="";
char packing;
char layerdone;
char evened;
char packingbest;
char hundredpercent;
char quit;

float boxx, boxy, boxz;
float bboxx, bboxy, bboxz;
float cboxx, cboxy, cboxz;
short int boxi, bboxi, cboxi;
float bfx, bfy, bfz;
float bbfx, bbfy, bbfz;
float xx, yy, zz;
float px, py, pz;

short int tbn;
short int x;
short int n;
float layerinlayer;
float prelayer;
float lilz;
short int itenum;
short int hour;
short int min;
short int sec;
short int layersindex;
float remainpx, remainpy, remainpz;
float packedy;
float prepackedy;
float layerthickness;
short int itelayer;
float preremainpy;
short int bestite;
short int packednumbox;
short int bestpackednum;

double packedvolume;
double bestvolume;
double totalvolume;
double totalboxvol;
double temp;
double percentageused;
double percentagepackedbox;
double elapsedtime;

#define T_start 100.0//initial temperature
#define q 0.5//annealing coefficient
double T;//temerature used by simulated annealing

struct boxinfo { 
  char packst;
  float dim1, dim2, dim3, cox, coy, coz, packx, packy, packz;
  short int n;
  float vol; 
} boxlist[5000];

struct layerlist{
  float layereval;
  float layerdim; 
} layers[1000];

struct scrappad{
  struct scrappad *pre, *pos;
  float cumx, cumz;
};

struct scrappad *scrapfirst, *scrapmemb, *smallestz, *trash; 

time_t start, finish;

FILE *ifp, *ofp;

//********************************************************
// MAIN PROGRAM
//********************************************************

int main(int argc, char *argv[]) 
{ 
  srand(time(NULL));
  if (argc == 1)
  {
    printf("(ASSUMED TO HAVE '.TXT' EXTENSION; UP TO 8 CHARACTERS LONG)\n");
    printf ("PLEASE ENTER THE NAME OF THE INPUT FILE :"); 
    scanf ("%s",filename);
  }
  else 
  {
    printf("%s", argv[1]);
    strcpy(filename, argv[1]);
  } 
  
  initialize();
  time(&start);
  printf("\nPRESS Q TO QUIT AT ANYTIME AND WAIT\n\n"); 
  execiterations();
  time(&finish);
  report();
  getch();
  return 0;
}

//********************************************************
// PERFORMS INITIALIZATIONS
//********************************************************

void initialize(void) 
{ 
  if (filename == "")
  {
    printf("\nINVALID FILE NAME\n"); 
    exit(1);
  } 
  inputboxlist();
  temp = 1.0; 
  totalvolume = temp * xx * yy * zz;
  totalboxvol = 0.0;
  for (x=1; x <= tbn; x++) {
    totalboxvol = totalboxvol + boxlist[x].vol; 
  }
  
  scrapfirst = malloc(sizeof(struct scrappad));
  
  if ((*scrapfirst).pos == NULL) 
  {
    printf("Insufficient memory available\n"); 
    exit(1);
  } 
  (*scrapfirst).pre = NULL;
  (*scrapfirst).pos = NULL;
  bestvolume = 0.0; 
  packingbest = 0;
  hundredpercent = 0;
  itenum = 0;
  quit = 0;
  strcat(filename, ".out");
  if ( (ofp = fopen(filename,"w")) == NULL ) 
  {
    printf("Cannot open file %s", filename);
    exit(1);
  }
  
}
         
         
//**********************************************************************
// READS THE PALLET AND BOX SET DATA ENTERED BY THE USER FROM 
// THE INPUT FILE
//**********************************************************************

void inputboxlist(void)
{
  short int n;
  char lbl[10], dim1[10], dim2[10], dim3[10], boxn[5], strxx[10], stryy[10], strzz[10];
  
  strcpy(strtemp, filename);
  strcat(strtemp, ".txt");
  
  if ( (ifp=fopen(strtemp,"r")) == NULL ) 
  {
    printf("Cannot open file %s", strtemp); 
    exit(1);
  }
  tbn = 1;
  
  if ( fscanf(ifp,"%s %s %s",strxx, stryy, strzz) == EOF )
  {
    exit(1);
  } 
  
  xx = atof(strxx); 
  yy = atof(stryy);
  zz = atof(strzz);
  printf("the three dims of the truck are: %02f,%02f,%02f",xx,yy,zz);
  while ( fscanf(ifp,"%s %s %s %s %s",lbl,dim1,dim2,dim3,boxn) != EOF )
  {
    boxlist[tbn].dim1 = atof(dim1);
    boxlist[tbn].dim2 = atof(dim2);
    boxlist[tbn].dim3 = atof(dim3);
    
    boxlist[tbn].vol = boxlist[tbn].dim1 * boxlist[tbn].dim2 * boxlist[tbn].dim3; 
    n = atoi(boxn); 
    boxlist[tbn].n = n;
    
    while (--n)
    {
      boxlist[tbn+n] = boxlist[tbn];
    }
    tbn = tbn+atoi(boxn);
  } 
  --tbn;
  fclose(ifp); 
  return;
}

//**********************************************************************
// ITERATIONS ARE DONE AND PARAMETERS OF THE BEST SOLUTION ARE 
// FOUND
//**********************************************************************

float dynamiccalclayerthick(short int current_box_index,float remaining_y)
{
  float candidate;
  //find the min dim of a box
  if(boxlist[current_box_index].dim1>boxlist[current_box_index].dim2)
    candidate=(boxlist[current_box_index].dim2<boxlist[current_box_index].dim3)?boxlist[current_box_index].dim2:boxlist[current_box_index].dim3;
  else
    candidate=(boxlist[current_box_index].dim1<boxlist[current_box_index].dim3)?boxlist[current_box_index].dim1:boxlist[current_box_index].dim3;
  if(candidate<=remaining_y)//we can generate a new layer which layer thickness is candidate
    return candidate;
  return -1;//this box can't be stored at a new layer, drop it
}

void dynamic_find_box(short int arriving_box_indx,float hmx, float hy, float hmy, float hz, float hmz)//given a box index, find out which rotation is the most suitable
{
  bfx = 32767; bfy = 32767; bfz = 32767; 
  bbfx = 32767; bbfy = 32767; bbfz = 32767; 
  boxi = 0; bboxi = 0;
  x = arriving_box_indx;
  analyzebox(hmx, hy, hmy, hz, hmz, boxlist[x].dim1, boxlist[x].dim2, boxlist[x].dim3);
  if ( (boxlist[x].dim1 == boxlist[x].dim3) && (boxlist[x].dim3 == boxlist[x].dim2) )
    return;
  analyzebox(hmx, hy, hmy, hz, hmz, boxlist[x].dim1, boxlist[x].dim3, boxlist[x].dim2);
  analyzebox(hmx, hy, hmy, hz, hmz, boxlist[x].dim2, boxlist[x].dim1, boxlist[x].dim3);
  analyzebox(hmx, hy, hmy, hz, hmz, boxlist[x].dim2, boxlist[x].dim3, boxlist[x].dim1);
  analyzebox(hmx, hy, hmy, hz, hmz, boxlist[x].dim3, boxlist[x].dim1, boxlist[x].dim2);
  analyzebox(hmx, hy, hmy, hz, hmz, boxlist[x].dim3, boxlist[x].dim2, boxlist[x].dim1);
}

char simulated_anneal(float increasement)
{
  double r;
  if (increasement > 0)//Metropolis criterion accept the increasement of the layerthickness with a certain probability
  {
      r = (double)rand() / (RAND_MAX);
      printf("\nsilulated anneal:increase %02f,T %02f, exp(-increasement / T) %02f,r %02f\n",increasement,T,exp(-increasement / T),r);
      if (exp(-increasement / T) <= r)//when the temperature is high, we can accept large increasement; when it's low, the thickness can hardly increase
          return 0;//discard the increasement
      T *= q;//cool down everytime we accepts an increasement
      return 1;//accept the increasement
  }
  return 0;//the increasement should be positive
}

short int dynamic_pack_box(short int box_index)
{
  float lenx, lenz, lpz;
  if (!layerthickness) 
  { 
    packing = 0;
    return 0;
  } 
  //for all gaps in a layer, find whether the box can be placed in the gap
  for(;!quit;)
  {
    findsmallestz();
    if (!(*smallestz).pre && !(*smallestz).pos)
    {
      //*** SITUATION-1: NO BOXES ON THE RIGHT AND LEFT SIDES ***
      
      lenx = (*smallestz).cumx;
      lpz = remainpz - (*smallestz).cumz;
      dynamic_find_box(box_index, lenx, layerthickness, remainpy, lpz, lpz); 
      checkfound();
      
      if (layerdone) break;
      if (evened) continue;
      
      boxlist[cboxi].cox = 0;
      boxlist[cboxi].coy = packedy; 
      boxlist[cboxi].coz = (*smallestz).cumz;
      if (cboxx == (*smallestz).cumx)
      {
        (*smallestz).cumz = (*smallestz).cumz + cboxz;
      }
      else 
      {
        (*smallestz).pos = malloc(sizeof(struct scrappad)); 
        if ((*smallestz).pos == NULL) 
        {
          printf("Insufficient memory available\n"); 
          return 1;
        } 
        (*((*smallestz).pos)).pos = NULL;
        (*((*smallestz).pos)).pre = smallestz; 
        (*((*smallestz).pos)).cumx = (*smallestz).cumx; 
        (*((*smallestz).pos)).cumz = (*smallestz).cumz; 
        (*smallestz).cumx = cboxx; 
        (*smallestz).cumz = (*smallestz).cumz + cboxz;
      } 
      volumecheck();
      break;
    }
    else if (!(*smallestz).pre) 
    {
      //*** SITUATION-2: NO BOXES ON THE LEFT SIDE ***
      
      lenx = (*smallestz).cumx;
      lenz = (*((*smallestz).pos)).cumz - (*smallestz).cumz; 
      lpz = remainpz - (*smallestz).cumz;
      dynamic_find_box(box_index, lenx, layerthickness, remainpy, lenz, lpz); 
      checkfound();
      
      if (layerdone) break;
      if (evened) continue;
      
      boxlist[cboxi].coy = packedy; 
      boxlist[cboxi].coz = (*smallestz).cumz; 
      if (cboxx == (*smallestz).cumx) 
      {
        boxlist[cboxi].cox = 0;
        if ( (*smallestz).cumz + cboxz == (*((*smallestz).pos)).cumz )
        { 
          (*smallestz).cumz = (*((*smallestz).pos)).cumz; 
          (*smallestz).cumx = (*((*smallestz).pos)).cumx; 
          trash = (*smallestz).pos; 
          (*smallestz).pos = (*((*smallestz).pos)).pos;
          if ((*smallestz).pos) 
          {
            (*((*smallestz).pos)).pre = smallestz;
          }
          free(trash);
        }
        else 
        {
          (*smallestz).cumz = (*smallestz).cumz + cboxz;
        }
      }
      else 
      {
        boxlist[cboxi].cox = (*smallestz).cumx - cboxx; 
        if ( (*smallestz).cumz + cboxz == (*((*smallestz).pos)).cumz )
        {
          (*smallestz).cumx = (*smallestz).cumx - cboxx;
        }
        else 
        {
          (*((*smallestz).pos)).pre = malloc(sizeof(struct scrappad));
          if ((*((*smallestz).pos)).pre == NULL) 
          { 
            printf("Insufficient memory available\n"); 
            return 1;
          } 
          (*((*((*smallestz).pos)).pre)).pos = (*smallestz).pos;
          (*((*((*smallestz).pos)).pre)).pre = smallestz;
          (*smallestz).pos = (*((*smallestz).pos)).pre; 
          (*((*smallestz).pos)).cumx = (*smallestz).cumx;
          (*smallestz).cumx = (*smallestz).cumx - cboxx; 
          (*((*smallestz).pos)).cumz = (*smallestz).cumz + cboxz;
        }
      } 
      volumecheck();
      break;
    }
    else if (!(*smallestz).pos)
    {
      //*** SITUATION-3: NO BOXES ON THE RIGHT SIDE ***
      
      lenx = (*smallestz).cumx - (*((*smallestz).pre)).cumx; 
      lenz = (*((*smallestz).pre)).cumz - (*smallestz).cumz; 
      lpz = remainpz - (* smallestz).cumz;
      dynamic_find_box(box_index, lenx, layerthickness, remainpy, lenz, lpz); 
      checkfound();
      
      if (layerdone) break;
      if (evened) continue;
      
      boxlist[cboxi].coy = packedy; 
      boxlist[cboxi].coz = (*smallestz).cumz;
      boxlist[cboxi].cox = (*((*smallestz).pre)).cumx;
      
      if (cboxx == (*smallestz).cumx - (*((*smallestz).pre)).cumx) 
      {
        if ( (*smallestz).cumz + cboxz == (*((*smallestz).pre)).cumz )
        { 
          (*((*smallestz).pre)).cumx = (*smallestz).cumx; 
          (*((*smallestz).pre)).pos = NULL;
          free(smallestz);
        } 
        else 
        {
          (*smallestz).cumz = (*smallestz).cumz + cboxz;
        }
      }
      else 
      {
        if ( (*smallestz).cumz + cboxz == (*((*smallestz).pre)).cumz )
        {
          (*((*smallestz).pre)).cumx = (*((*smallestz).pre)).cumx + cboxx;
        }
        else 
        {
          (*((*smallestz).pre)).pos = malloc(sizeof(struct scrappad));
          if ( (*((*smallestz).pre)).pos == NULL ) 
          {
            printf("Insufficient memory available\n"); 
            return 1;
          }
          (*((*((*smallestz).pre)).pos)).pre = (*smallestz).pre;
          (*((*((*smallestz).pre)).pos)).pos = smallestz; 
          (*smallestz).pre = (*((*smallestz).pre)).pos; 
          (*((*smallestz).pre)).cumx = (*((*((*smallestz).pre)).pre)).cumx + cboxx; 
          (*((*smallestz).pre)).cumz = (*smallestz).cumz + cboxz;
        }
      } 
      volumecheck();
      break;
    }
    else if ( (*((*smallestz).pre)).cumz == (*((*smallestz).pos)).cumz ) 
    {
      //*** SITUATION-4: THERE ARE BOXES ON BOTH OF THE SIDES *** 
      
      //*** SUBSITUATION-4A: SIDES ARE EQUAL TO EACH OTHER ***
      
      lenx = (*smallestz).cumx - (*((*smallestz).pre)).cumx; 
      lenz = (*((*smallestz).pre)).cumz - (*smallestz).cumz;
      lpz = remainpz - (*smallestz).cumz;
      
      dynamic_find_box(box_index, lenx, layerthickness, remainpy, lenz, lpz); 
      checkfound();
      
      if (layerdone) break;
      if (evened) continue;
      
      boxlist[cboxi].coy = packedy;
      boxlist[cboxi].coz = (*smallestz).cumz; 
      if ( cboxx == (*smallestz).cumx - (*((*smallestz).pre)).cumx ) 
      {
        boxlist[cboxi].cox = (*((*smallestz).pre)).cumx; 
        if ( (*smallestz).cumz + cboxz == (*((*smallestz).pos)).cumz )
        {
          (*((*smallestz).pre)).cumx = (*((*smallestz).pos)).cumx;
          if ( (*((*smallestz).pos)).pos ) 
          { 
            (*((*smallestz).pre)).pos = (*((*smallestz).pos)).pos; 
            (*((*((*smallestz).pos)).pos)).pre = (*smallestz).pre;
            free(smallestz);
          }
          else 
          {
            (*((*smallestz).pre)).pos = NULL;
            free(smallestz);
          }
        } 
        else
        {
          (*smallestz).cumz = (*smallestz).cumz + cboxz;
        }
      }
      else if ( (*((*smallestz).pre)).cumx < px - (*smallestz).cumx ) 
      {
        if ( (*smallestz).cumz + cboxz == (*((*smallestz).pre)).cumz)
        { 
          (*smallestz).cumx = (*smallestz).cumx - cboxx; 
          boxlist[cboxi].cox = (*smallestz).cumx - cboxx;
        }
        else 
        {
          boxlist[cboxi].cox = (*((*smallestz).pre)).cumx; 
          (*((*smallestz).pre)).pos = malloc(sizeof(struct scrappad)); 
          if ( (*((*smallestz).pre)).pos == NULL ) 
          {
            printf("Insufficient memory available\n"); 
            return 1;
          } 
          (*((*((*smallestz).pre)).pos)).pre = (*smallestz).pre;
          (*((*((*smallestz).pre)).pos)).pos = smallestz;
          (*smallestz).pre = (*((*smallestz).pre)).pos;
          (*((*smallestz).pre)).cumx = (*((*((*smallestz).pre)).pre)).cumx + cboxx;
          (*((*smallestz).pre)).cumz = (*smallestz).cumz + cboxz;
        }
      }
      else 
      {
        if ( (*smallestz).cumz + cboxz == (*((*smallestz).pre)).cumz )
        { 
          (*((*smallestz).pre)).cumx = (*((*smallestz).pre)).cumx + cboxx; 
          boxlist[cboxi].cox = (*((*smallestz).pre)).cumx;
        }
        else 
        {
          boxlist[cboxi].cox = (*smallestz).cumx - cboxx;
          (*((*smallestz).pos)).pre = malloc(sizeof(struct scrappad));
          if ((*((*smallestz).pos)).pre == NULL) 
          {
            printf("Insufficient memory available\n"); 
            return 1;
          }
          (*((*((*smallestz).pos)).pre)).pos = (*smallestz).pos;
          (*((*((*smallestz).pos)).pre)).pre = smallestz;
          (*smallestz).pos = (*((*smallestz).pos)).pre;
          (*((*smallestz).pos)).cumx = (*smallestz).cumx;
          (*((*smallestz).pos)).cumz = (*smallestz).cumz + cboxz; 
          (*smallestz).cumx = (*smallestz).cumx - cboxx;
        }
      } 
      volumecheck();
      break;
    }
    else 
    {
      //*** SUBSITUATION-4B: SIDES ARE NOT EQUAL TO EACH OTHER ***
      
      lenx = (*smallestz).cumx - (*((*smallestz).pre)).cumx;
      lenz = (*((*smallestz).pre)).cumz - (*smallestz).cumz;
      lpz = remainpz - (*smallestz).cumz;
      dynamic_find_box(box_index, lenx, layerthickness, remainpy, lenz, lpz);
      checkfound();
      
      if (layerdone) break;
      if (evened) continue;
      
      boxlist[cboxi].coy = packedy;
      boxlist[cboxi].coz = (*smallestz).cumz;
      boxlist[cboxi].cox = (*((*smallestz).pre)).cumx;
      if ( cboxx == (*smallestz).cumx - (*((*smallestz).pre)).cumx )
      {
        if ((*smallestz).cumz + cboxz == (*((*smallestz).pre)).cumz)
        { 
          (*((*smallestz).pre)).cumx = (*smallestz).cumx; 
          (*((*smallestz).pre)).pos = (*smallestz).pos;
          (*((*smallestz).pos)).pre = (*smallestz).pre;
          free(smallestz);
        } 
        else
        {
          (*smallestz).cumz = (*smallestz).cumz + cboxz;
        }
      }
      else 
      {
        if ( (*smallestz).cumz + cboxz == (*((*smallestz).pre)).cumz )
        {
          (*((*smallestz).pre)).cumx = (*((*smallestz).pre)).cumx + cboxx;
        } 
        else if ( (*smallestz).cumz + cboxz == (*((*smallestz).pos)).cumz )
        { 
          boxlist[cboxi].cox = (*smallestz).cumx - cboxx;
          (*smallestz).cumx = (*smallestz).cumx - cboxx;
        }
        else
        {
          (*((*smallestz).pre)).pos = malloc(sizeof(struct scrappad));
          if ( (*((*smallestz).pre)).pos == NULL ) 
          { 
            printf("Insufficient memory available\n");
            return 1;
          }
          (*((*((*smallestz).pre)).pos)).pre = (*smallestz).pre;
          (*((*((*smallestz).pre)).pos)).pos = smallestz;
          (*smallestz).pre = (*((*smallestz).pre)).pos;
          (*((*smallestz).pre)).cumx = (*((*((*smallestz).pre)).pre)).cumx + cboxx;
          (*((*smallestz).pre)).cumz = (*smallestz).cumz + cboxz;
        }
      }
      volumecheck();
      break;
    }
  }
  return 0;
}

void execiterations(void) 
{
  px=xx; py=yy; pz=zz; 
  //initialize layer thickness by considering all boxes
  //listcanditlayers();
  //layers[0].layereval = -1;
  //qsort(layers, layerlistlen+1, sizeof(struct layerlist), complayerlist);
  ++itenum;
  time(&finish);
  elapsedtime = difftime(finish, start);
  printf("ITERATION (TOTAL): %5d; BEST SO FAR: %.3f %%; TIME: %.0f", itenum, percentageused, elapsedtime); 
  packedvolume = 0.0;
  packedy = 0;
  packing = 1;
  short int dynamic_box_arrived=0;
  itelayer = layersindex;
  remainpy = py; 
  remainpz = pz;
  packednumbox = 0;
  for (x = 1; x <= tbn; x++)
  {
    boxlist[x].packst=0;
  }
  gcvt(px,5,strpx);
  gcvt(py,5,strpy);
  gcvt(pz,5,strpz);
  
  fprintf(ofp,"%10s%10s%10s\n", strpx, strpy, strpz); 
  //BEGIN DO-WHILE
  layersindex=1;
  char should_recover_layer_in_layer=0;
  T = T_start;
  do
  {
    dynamic_box_arrived+=1;
    //printf("box arrived %d\n",dynamic_box_arrived);
    if(dynamic_box_arrived>tbn)
      break;
    short int i=layersindex-1;
    if(i>0)
    {
      layerdone = 0;
      layerthickness=layers[i].layerdim;
      //printf("fill orig layer:box %d,remainpy %02f, layer thickness %02f\n",dynamic_box_arrived,remainpy,layerthickness);
      
      dynamic_pack_box(dynamic_box_arrived);
      //printf("is_packed:%d,dy:%d\n",boxlist[dynamic_box_arrived].packst,remainpy);
    }
    if(boxlist[dynamic_box_arrived].packst==1)//the box is packed
      continue;
    if(layersindex!=1 && ((layerinlayer<0.1 && layerinlayer>-0.1) || !should_recover_layer_in_layer))//every time when we finished packing a layer and need to add a new layer
    {
      packedy = packedy + layerthickness;
      remainpy = py - packedy;
      T = T_start;
      if(remainpy<0)
        break;
    }
    //layerinlayer, a box can only be packed in a new layer which height is the increasement of the layerthichness
    //since remain_y is now limited, now a box can never set layer_in_layer=true
    if (layerinlayer>0.1 && !should_recover_layer_in_layer)
    {
      should_recover_layer_in_layer=1;
      prepackedy = packedy; 
      preremainpy = remainpy; 
      remainpy = layerthickness - prelayer; 
      packedy = packedy - layerthickness + prelayer;
      remainpz = lilz;
      layerthickness = layerinlayer;
      layers[i].layerdim=layerinlayer;
      layerdone = 0;
      //printf("\nlayerinlayer start info %02f %02f %02f\n",layerthickness,prelayer,prepackedy);
      //printf("%02f %02f %02f",remainpy,packedy,preremainpy);
      (*scrapfirst).cumx = px;
      (*scrapfirst).cumz = 0;
      dynamic_pack_box(dynamic_box_arrived);
      if(boxlist[dynamic_box_arrived].packst==1)//the box is packed
        continue;
    }
    if(should_recover_layer_in_layer)
    {
      should_recover_layer_in_layer=0;
      packedy = prepackedy; 
      remainpy = preremainpy;
      remainpz = pz;
    }
    //the box cannot be packed in the current layer, generate a new layer
    layerthickness=dynamiccalclayerthick(dynamic_box_arrived,remainpy);
    if(layerthickness==-1)//the box cannot be placed in a new layer, drop it
      continue;
    layers[layersindex].layerdim=layerthickness;
    
    layerinlayer = 0;
    layerdone = 0;
    (*scrapfirst).cumx = px;
    (*scrapfirst).cumz = 0;
    layersindex+=1;
    dynamic_pack_box(dynamic_box_arrived);
  }
  while (packing && !quit);
  // END DO-WHILE
  
  if ((packedvolume > bestvolume) && !quit) 
  { 
    bestvolume = packedvolume;
    bestite = itelayer; 
    bestpackednum = packednumbox;
  }

  percentageused = bestvolume * 100 / totalvolume; 
  printf("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b");
  printf("\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b\b");

}

//**********************************************************************
// ANALYZES EACH UNPACKED BOX TO FIND THE BEST FITTING ONE TO 
// THE EMPTY SPACE GIVEN
//**********************************************************************

void analyzebox(float hmx, float hy, float hmy, float hz, float hmz, float dim1, float dim2, float dim3)
{
  if (dim1 <= hmx && dim2 <= hmy && dim3 <= hmz) 
  {
    if (dim2 <= hy) 
    {
      if (hy - dim2 < bfy) 
      {
        boxx = dim1; 
        boxy = dim2; 
        boxz = dim3;
        bfx = hmx - dim1;
        bfy = hy - dim2;
        bfz = abs(hz - dim3);
        boxi = x;
      }
      else if (hy - dim2 == bfy && hmx - dim1 < bfx) 
      {
        boxx = dim1; 
        boxy = dim2;
        boxz = dim3;
        bfx = hmx - dim1;
        bfy = hy - dim2;
        bfz = abs(hz - dim3);
        boxi = x;
      }
      else if (hy - dim2 == bfy && hmx - dim1 == bfx && abs(hz - dim3) < bfz)
      {
        boxx = dim1;
        boxy = dim2;
        boxz = dim3;
        bfx = hmx - dim1; 
        bfy = hy - dim2; 
        bfz = abs(hz - dim3);
        boxi = x;
      }
    }
    else 
    {
      if (dim2 - hy < bbfy) 
      {
        bboxx = dim1;
        bboxy = dim2;
        bboxz = dim3;
        bbfx = hmx - dim1;
        bbfy = dim2-hy;
        bbfz = abs(hz - dim3);
        bboxi = x;
      }
      else if (dim2 - hy == bbfy && hmx - dim1 < bbfx) 
      {
        bboxx = dim1;
        bboxy = dim2;
        bboxz = dim3;
        bbfx = hmx - dim1;
        bbfy = dim2 - hy;
        bbfz = abs(hz - dim3);
        bboxi = x;
      }
      else if (dim2 - hy == bbfy && hmx-dim1 == bbfx && abs(hz - dim3) < bbfz) 
      { 
        bboxx = dim1;
        bboxy = dim2;
        bboxz = dim3;
        bbfx = hmx - dim1;
        bbfy = dim2 - hy;
        bbfz = abs(hz - dim3);
        bboxi = x;
      }
    }
  }
}
            
//********************************************************
// FINDS THE FIRST TO BE PACKED GAP IN THE LAYER EDGE
//********************************************************
void findsmallestz(void) 
{ 
  scrapmemb = scrapfirst;
  smallestz = scrapmemb;
  while ( !((*scrapmemb).pos == NULL))
  { 
    if ( (*((*scrapmemb).pos)).cumz < (*smallestz).cumz )
    {
      smallestz = (*scrapmemb).pos;
    }
    scrapmemb = (*scrapmemb).pos;
  } 
  return;
} 

//************************************************************
// AFTER FINDING EACH BOX, THE CANDIDATE BOXES AND THE 
// CONDITION OF THE LAYER ARE EXAMINED
//************************************************************

void checkfound(void)
{ 
  evened = 0;
  if (boxi) 
  { 
    cboxi = boxi;
    cboxx = boxx;
    cboxy = boxy;
    cboxz = boxz;
  }
  else 
  {
    if ( (bboxi > 0) && (layerinlayer>0.1 || (!(*smallestz).pre && !(*smallestz).pos)) )
    {
      if(!simulated_anneal(bboxy - layerthickness))
        return;
      if ((layerinlayer<0.1 && layerinlayer>-0.1)) 
      {
        prelayer = layerthickness;
        lilz = (*smallestz).cumz;
      }
      cboxi = bboxi;
      cboxx = bboxx;
      cboxy = bboxy;
      cboxz = bboxz;
      layerinlayer = layerinlayer + bboxy - layerthickness;
      //printf("\nlayerinlayer %.2f\n",layerinlayer);
      layerthickness = bboxy;
      layers[layersindex-1].layerdim=layerthickness;
    }
    else
    {
      if ( !(*smallestz).pre && !(*smallestz).pos )
      {
        layerdone = 1; 
      }
      else 
      {
        evened = 1;
        if (!(*smallestz).pre) 
        {
          trash = (*smallestz).pos; 
          (*smallestz).cumx = (*((*smallestz).pos)).cumx;
          (*smallestz).cumz = (*((*smallestz).pos)).cumz; 
          (*smallestz).pos = (*((*smallestz).pos)).pos;
          if ((*smallestz).pos)
          {
            (*((*smallestz).pos)).pre = smallestz;
          }
          free(trash);
        }
        else if (!(*smallestz).pos)
        {
          (*((*smallestz).pre)).pos = NULL; 
          (*((*smallestz).pre)).cumx = (*smallestz).cumx;
          free(smallestz);
        }
        else 
        {
          if ( (*((*smallestz).pre)).cumz == (*((*smallestz).pos)).cumz ) 
          {
            (*((*smallestz).pre)).pos = (*((*smallestz).pos)).pos;
            if ((*((*smallestz).pos)).pos)
            {
              (*((*((*smallestz).pos)).pos)).pre = (*smallestz).pre;
            } 
            (*((*smallestz).pre)).cumx = (*((*smallestz).pos)).cumx;
            free((*smallestz).pos);
            free(smallestz);
          }
          else
          {
            (*((*smallestz).pre)).pos = (*smallestz).pos; 
            (*((*smallestz).pos)).pre = (*smallestz).pre;
            if ((*((*smallestz).pre)).cumz < (*((*smallestz).pos)).cumz) 
            {
              (*((*smallestz).pre)).cumx = (*smallestz).cumx;
            }
            free(smallestz);
          }
        } 
      }
    }
  }
  return;
}

//********************************************************************
// AFTER PACKING OF EACH BOX, 100% PACKING CONDITION IS CHECKED
//********************************************************************

void volumecheck (void) 
{
  boxlist[cboxi].packst = 1;
  boxlist[cboxi].packx = cboxx;
  boxlist[cboxi].packy = cboxy;
  boxlist[cboxi].packz = cboxz;
  packedvolume = packedvolume + boxlist[cboxi].vol;
  packednumbox++;

  outputsolution();

  if (packedvolume == totalvolume || packedvolume == totalboxvol) 
  {
    packing = 0; 
    hundredpercent = 1;
  } 
  return;
}

//*********************************************************************
// output packed information
//*********************************************************************

void outputsolution(void) 
{ 
  char n[5];

  gcvt(boxlist[cboxi].cox,5,strcox);
  gcvt(boxlist[cboxi].coy,5,strcoy);
  gcvt(boxlist[cboxi].coz,5,strcoz);
  gcvt(boxlist[cboxi].packx,5,strpackx);
  gcvt(boxlist[cboxi].packy,5,strpacky);
  gcvt(boxlist[cboxi].packz,5,strpackz);

  fprintf(ofp, "%10s%10s%10s%10s%10s%10s\n", strcox, strcoy, strcoz, strpackx, strpacky, strpackz);
}
  
//*******************************************************************
// USING THE PARAMETERS FOUND, PACKS THE BEST SOLUTION FOUND 
// AND REPORS TO THE CONSOLE AND TO A TEXT FILE
//*******************************************************************

void report(void)
{ 
  quit = 0;
  
  percentagepackedbox = bestvolume * 100 / totalboxvol;
  percentageused = bestvolume * 100 / totalvolume;
  elapsedtime = difftime( finish, start);

  fclose(ofp);
  printf("\n");
  for (n = 1; n <= tbn; n++)
  {
    if (boxlist[n].packst)
    {
      printf("%d %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f %.2f\n", n, boxlist[n].dim1, boxlist[n].dim2, boxlist[n].dim3, boxlist[n].cox, boxlist[n].coy, boxlist[n].coz, boxlist[n].packx, boxlist[n].packy, boxlist[n].packz);
    }
  }
  printf("ELAPSED TIME                       : Almost %.0f sec\n", elapsedtime);
  printf("TOTAL NUMBER OF ITERATIONS DONE    : %d\n", itenum);
  printf("TOTAL NUMBER OF BOXES              : %d\n", tbn); 
  printf("PACKED NUMBER OF BOXES             : %d\n", bestpackednum);
  printf("TOTAL VOLUME OF ALL BOXES          : %.2f\n", totalboxvol);
  printf("PALLET VOLUME                      :%.2f\n",totalvolume); 
  printf("BEST SOLUTION'S VOLUME UTILIZATION :%.2f OUT OF %.2f\n", bestvolume, totalvolume);
  printf("PERCENTAGE OF PALLET VOLUME USED   : %.6f %%\n", percentageused);
  printf("PERCENTAGE OF PACKEDBOXES (VOLUME) :%.6f%%\n", percentagepackedbox);
}
