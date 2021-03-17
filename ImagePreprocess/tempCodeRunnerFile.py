output_image=np.ones((hb,wb,3))*100
for k in range(0,wb):
    for l in range(0,hb):
        a=k*wr_min
        b=l*wr_min
        if (a+b-0.1)<w or (w+a-0.1)<b or (w+b-0.1)<a:
            continue
        x=(a**2+w**2-b**2)/(2*w)
        y=math.sqrt((a*w)**2-((w**2+a**2-b**2)/2)**2)/w
        if x>=x1 and y>=y1:
            m=int((x-x1)/wg)
            n=int((y-y1)/wg)
            if m<wi and n<hi:
                output_image[l,k]=input_image[n,m]